# Tech Starter UBSI one-command installer for Windows.
#
# One command:
#   irm https://raw.githubusercontent.com/ruhulikram/techstarter-ubsi/main/install.ps1 | iex

[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$NonInteractive,
    [switch]$SkipBrowser
)

$ErrorActionPreference = 'Stop'

$RepoRaw = 'https://raw.githubusercontent.com/ruhulikram/techstarter-ubsi/main'
$ManifestUrl = "$RepoRaw/config/packages.json"

function Write-Section {
    param([string]$Title)

    Write-Host ''
    Write-Host '============================================================'
    Write-Host $Title
    Write-Host '============================================================'
}

function Assert-Windows {
    if (-not $IsWindows -and $PSVersionTable.PSEdition -eq 'Core') {
        throw 'Installer ini hanya mendukung Windows. macOS installer akan dibuat pada fase berikutnya.'
    }
}

function Get-PackageManifest {
    $localManifest = Join-Path $PSScriptRoot 'config\packages.json'

    if ($PSScriptRoot -and (Test-Path -LiteralPath $localManifest)) {
        Write-Host "Menggunakan manifest lokal: $localManifest"
        return Get-Content -Raw -LiteralPath $localManifest | ConvertFrom-Json
    }

    Write-Host "Mengambil manifest dari GitHub: $ManifestUrl"
    return Invoke-RestMethod -Uri $ManifestUrl
}

function Test-CommandAvailable {
    param([string]$Command)

    return $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

function Test-WingetPackageInstalled {
    param([string]$PackageId)

    $output = & winget list --id $PackageId --exact --source winget 2>$null
    return $LASTEXITCODE -eq 0 -and ($output -match [regex]::Escape($PackageId))
}

function Install-WingetPackage {
    param(
        [string]$PackageId,
        [string]$PackageName
    )

    Write-Host "Menginstal $PackageName ($PackageId) ..."
    & winget install `
        --id $PackageId `
        --exact `
        --source winget `
        --accept-package-agreements `
        --accept-source-agreements

    if ($LASTEXITCODE -ne 0) {
        throw "Gagal menginstal $PackageName ($PackageId)."
    }
}

function Get-WindowsCorePackages {
    param($Manifest)

    $packages = @()
    foreach ($package in $Manifest.packages) {
        if (-not $package.mvpDefault) {
            continue
        }

        if ($SkipBrowser -and $package.key -eq 'browser') {
            continue
        }

        if ($package.platforms.windows.manager -ne 'winget') {
            continue
        }

        $packages += $package
    }

    return $packages
}

function Confirm-Install {
    param([array]$Packages)

    if ($NonInteractive -or $DryRun) {
        return
    }

    Write-Host ''
    Write-Host "Installer akan memproses $($Packages.Count) paket Core."
    $answer = Read-Host 'Lanjutkan instalasi? [Y/n]'
    if ($answer -and $answer.ToLowerInvariant() -notin @('y', 'yes')) {
        throw 'Instalasi dibatalkan oleh pengguna.'
    }
}

function Show-Summary {
    param(
        [array]$Installed,
        [array]$AlreadyInstalled,
        [array]$Failed,
        [array]$Skipped
    )

    Write-Section 'INSTALLATION SUMMARY'
    Write-Host "Installed         : $($Installed.Count)"
    Write-Host "Already installed : $($AlreadyInstalled.Count)"
    Write-Host "Failed            : $($Failed.Count)"
    Write-Host "Skipped           : $($Skipped.Count)"

    if ($Failed.Count -gt 0) {
        Write-Host ''
        Write-Host 'FAILED packages:'
        foreach ($item in $Failed) {
            Write-Host "- $item"
        }
    }

    Write-Host ''
    Write-Host 'Buka terminal baru setelah instalasi selesai agar PATH terbaru terbaca.'
}

try {
    Assert-Windows

    Write-Section 'Tech Starter UBSI'
    Write-Host 'One-command installer untuk paket Core Windows.'
    Write-Host 'Paket dipasang melalui WinGet dari sumber resmi.'

    $manifest = Get-PackageManifest
    $packages = Get-WindowsCorePackages -Manifest $manifest

    if ($packages.Count -eq 0) {
        throw 'Tidak ada paket Core Windows yang ditemukan di manifest.'
    }

    Write-Section 'PACKAGE PLAN'
    foreach ($package in $packages) {
        Write-Host "- $($package.name) [$($package.platforms.windows.id)]"
    }

    if (-not $DryRun -and -not (Test-CommandAvailable -Command 'winget')) {
        throw 'WinGet tidak ditemukan. Update App Installer dari Microsoft Store, lalu buka terminal baru.'
    }

    Confirm-Install -Packages $packages

    $installed = @()
    $alreadyInstalled = @()
    $failed = @()
    $skipped = @()

    foreach ($package in $packages) {
        $name = [string]$package.name
        $packageId = [string]$package.platforms.windows.id

        if ($DryRun) {
            Write-Host "DRY RUN: akan memproses $name ($packageId)"
            $skipped += $name
            continue
        }

        try {
            if (Test-WingetPackageInstalled -PackageId $packageId) {
                Write-Host "Sudah terpasang: $name"
                $alreadyInstalled += $name
                continue
            }

            Install-WingetPackage -PackageId $packageId -PackageName $name
            $installed += $name
        }
        catch {
            $failed += "$name - $($_.Exception.Message)"
            Write-Warning $_.Exception.Message
        }
    }

    Show-Summary `
        -Installed $installed `
        -AlreadyInstalled $alreadyInstalled `
        -Failed $failed `
        -Skipped $skipped

    if ($failed.Count -gt 0) {
        exit 1
    }

    exit 0
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}

