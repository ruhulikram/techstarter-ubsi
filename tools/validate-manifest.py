#!/usr/bin/env python3
"""Validate Tech Starter UBSI manifests without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
KEY_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ALLOWED_CATEGORIES = {"browser", "developer-tool", "editor", "language", "utility"}
ALLOWED_MANAGERS = {"brew", "brew-cask", "manual", "winget"}
ALLOWED_PROFILE_STATUS = {"active", "planned"}


class ValidationError(Exception):
    """Raised when a manifest validation rule fails."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise ValidationError(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValidationError(f"{path} must contain a JSON object")
    return data


def require_keys(item: dict[str, Any], keys: set[str], label: str) -> None:
    missing = keys - item.keys()
    if missing:
        raise ValidationError(f"{label} missing required keys: {', '.join(sorted(missing))}")


def ensure_key(value: Any, label: str) -> str:
    if not isinstance(value, str) or not KEY_RE.fullmatch(value):
        raise ValidationError(f"{label} must use lowercase letters, numbers, and hyphens")
    return value


def ensure_bool(value: Any, label: str) -> None:
    if not isinstance(value, bool):
        raise ValidationError(f"{label} must be a boolean")


def ensure_non_empty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be a non-empty string")
    return value


def ensure_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ValidationError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    result: list[str] = []
    for index, item in enumerate(value):
        result.append(ensure_key(item, f"{label}[{index}]"))
    return result


def ensure_unique(values: list[str], label: str) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    if duplicates:
        raise ValidationError(f"{label} contains duplicates: {', '.join(sorted(duplicates))}")


def validate_packages(packages_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    require_keys(packages_data, {"schemaVersion", "packages"}, "packages.json")
    packages = packages_data["packages"]
    if not isinstance(packages, list) or not packages:
        raise ValidationError("packages.json packages must be a non-empty list")

    package_keys: list[str] = []
    package_map: dict[str, dict[str, Any]] = {}
    required_keys = {
        "key",
        "name",
        "description",
        "category",
        "profiles",
        "minimumSemester",
        "required",
        "heavy",
        "manual",
        "mvpDefault",
        "verification",
        "platforms",
    }

    for index, package in enumerate(packages):
        if not isinstance(package, dict):
            raise ValidationError(f"packages[{index}] must be an object")
        label = f"package {package.get('key', index)}"
        require_keys(package, required_keys, label)

        key = ensure_key(package["key"], f"{label}.key")
        package_keys.append(key)
        package_map[key] = package

        ensure_non_empty_string(package["name"], f"{label}.name")
        ensure_non_empty_string(package["description"], f"{label}.description")
        category = ensure_non_empty_string(package["category"], f"{label}.category")
        if category not in ALLOWED_CATEGORIES:
            raise ValidationError(f"{label}.category is not allowed: {category}")
        ensure_string_list(package["profiles"], f"{label}.profiles")

        semester = package["minimumSemester"]
        if not isinstance(semester, int) or not 1 <= semester <= 8:
            raise ValidationError(f"{label}.minimumSemester must be an integer from 1 to 8")

        for bool_key in ("required", "heavy", "manual", "mvpDefault"):
            ensure_bool(package[bool_key], f"{label}.{bool_key}")

        verification = package["verification"]
        if not isinstance(verification, list) or not verification:
            raise ValidationError(f"{label}.verification must be a non-empty list")
        for command in verification:
            ensure_non_empty_string(command, f"{label}.verification item")

        platforms = package["platforms"]
        if not isinstance(platforms, dict):
            raise ValidationError(f"{label}.platforms must be an object")
        for platform_name in ("windows", "macos"):
            platform = platforms.get(platform_name)
            if not isinstance(platform, dict):
                raise ValidationError(f"{label}.platforms.{platform_name} must be an object")
            require_keys(platform, {"manager", "id"}, f"{label}.platforms.{platform_name}")
            manager = ensure_non_empty_string(platform["manager"], f"{label}.{platform_name}.manager")
            if manager not in ALLOWED_MANAGERS:
                raise ValidationError(f"{label}.{platform_name}.manager is not allowed: {manager}")
            ensure_non_empty_string(platform["id"], f"{label}.{platform_name}.id")
            if "fallbackIds" in platform:
                fallback_ids = platform["fallbackIds"]
                if not isinstance(fallback_ids, list):
                    raise ValidationError(f"{label}.{platform_name}.fallbackIds must be a list")
                for fallback_id in fallback_ids:
                    ensure_non_empty_string(fallback_id, f"{label}.{platform_name}.fallbackIds item")

    ensure_unique(package_keys, "package keys")
    return package_map


def validate_profiles(
    profiles_data: dict[str, Any], package_keys: set[str]
) -> dict[str, dict[str, Any]]:
    require_keys(profiles_data, {"schemaVersion", "profiles"}, "profiles.json")
    profiles = profiles_data["profiles"]
    if not isinstance(profiles, list) or not profiles:
        raise ValidationError("profiles.json profiles must be a non-empty list")

    profile_keys: list[str] = []
    profile_map: dict[str, dict[str, Any]] = {}
    required_keys = {"key", "name", "description", "status", "packageKeys"}

    for index, profile in enumerate(profiles):
        if not isinstance(profile, dict):
            raise ValidationError(f"profiles[{index}] must be an object")
        label = f"profile {profile.get('key', index)}"
        require_keys(profile, required_keys, label)

        key = ensure_key(profile["key"], f"{label}.key")
        profile_keys.append(key)
        profile_map[key] = profile

        ensure_non_empty_string(profile["name"], f"{label}.name")
        ensure_non_empty_string(profile["description"], f"{label}.description")
        status = ensure_non_empty_string(profile["status"], f"{label}.status")
        if status not in ALLOWED_PROFILE_STATUS:
            raise ValidationError(f"{label}.status must be active or planned")

        package_refs = ensure_string_list(profile["packageKeys"], f"{label}.packageKeys", allow_empty=True)
        unknown = sorted(set(package_refs) - package_keys)
        if unknown:
            raise ValidationError(f"{label}.packageKeys references unknown packages: {', '.join(unknown)}")

    ensure_unique(profile_keys, "profile keys")
    if "core" not in profile_map:
        raise ValidationError("profiles.json must define the core profile")
    if profile_map["core"]["status"] != "active":
        raise ValidationError("core profile must be active")
    return profile_map


def validate_package_profile_links(
    package_map: dict[str, dict[str, Any]], profile_keys: set[str]
) -> None:
    for package_key, package in package_map.items():
        package_profiles = ensure_string_list(package["profiles"], f"package {package_key}.profiles")
        unknown = sorted(set(package_profiles) - profile_keys)
        if unknown:
            raise ValidationError(
                f"package {package_key}.profiles references unknown profiles: {', '.join(unknown)}"
            )


def validate_semesters(
    semesters_data: dict[str, Any], profile_keys: set[str], package_keys: set[str]
) -> None:
    require_keys(semesters_data, {"schemaVersion", "semesters"}, "semesters.json")
    semesters = semesters_data["semesters"]
    if not isinstance(semesters, list) or not semesters:
        raise ValidationError("semesters.json semesters must be a non-empty list")

    semester_numbers: list[int] = []
    required_keys = {"semester", "recommendedProfiles", "recommendedPackageKeys", "notes"}

    for index, semester in enumerate(semesters):
        if not isinstance(semester, dict):
            raise ValidationError(f"semesters[{index}] must be an object")
        label = f"semester {semester.get('semester', index)}"
        require_keys(semester, required_keys, label)

        semester_number = semester["semester"]
        if not isinstance(semester_number, int) or not 1 <= semester_number <= 8:
            raise ValidationError(f"{label}.semester must be an integer from 1 to 8")
        semester_numbers.append(semester_number)

        profile_refs = ensure_string_list(semester["recommendedProfiles"], f"{label}.recommendedProfiles")
        unknown_profiles = sorted(set(profile_refs) - profile_keys)
        if unknown_profiles:
            raise ValidationError(
                f"{label}.recommendedProfiles references unknown profiles: {', '.join(unknown_profiles)}"
            )

        package_refs = ensure_string_list(
            semester["recommendedPackageKeys"], f"{label}.recommendedPackageKeys", allow_empty=True
        )
        unknown_packages = sorted(set(package_refs) - package_keys)
        if unknown_packages:
            raise ValidationError(
                f"{label}.recommendedPackageKeys references unknown packages: {', '.join(unknown_packages)}"
            )

        ensure_non_empty_string(semester["notes"], f"{label}.notes")

    duplicate_semesters = sorted(
        number for number in set(semester_numbers) if semester_numbers.count(number) > 1
    )
    if duplicate_semesters:
        raise ValidationError(f"semesters.json contains duplicates: {duplicate_semesters}")


def main() -> int:
    try:
        packages = load_json(CONFIG / "packages.json")
        profiles = load_json(CONFIG / "profiles.json")
        semesters = load_json(CONFIG / "semesters.json")

        package_map = validate_packages(packages)
        profile_map = validate_profiles(profiles, set(package_map))
        validate_package_profile_links(package_map, set(profile_map))
        validate_semesters(semesters, set(profile_map), set(package_map))
    except ValidationError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1

    print("SUCCESS: manifests are valid")
    print(f"Packages : {len(package_map)}")
    print(f"Profiles : {len(profile_map)}")
    print(f"Semesters: {len(semesters['semesters'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

