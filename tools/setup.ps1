param([switch]$SkipLeetgo)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $repo
try {
    $env:GOBIN = Join-Path $repo '.tools'
    $env:GOMODCACHE = Join-Path $repo '.cache\go-mod'
    $env:GOCACHE = Join-Path $repo '.cache\go-build'
    $env:LEETGO_HOME = Join-Path $repo '.cache\leetgo'
    if (-not $SkipLeetgo) {
        go install github.com/j178/leetgo@v1.4.19
        if ($LASTEXITCODE -ne 0) { throw 'leetgo installation failed (Go 1.26+ required).' }
    }
    Push-Location -LiteralPath (Join-Path $repo 'go')
    try {
        go mod download
        if ($LASTEXITCODE -ne 0) { throw 'Go dependency download failed.' }
    } finally { Pop-Location }
    python -m venv python/.venv
    if ($LASTEXITCODE -ne 0) { throw 'Python virtual environment creation failed.' }
    & (Join-Path $repo 'python/.venv/Scripts/python.exe') -m pip install -r python/requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed.' }
    # Dependency revisions used by the pinned leetgo v1.4.19. Avoid recreating
    # the venv or Go module the next time leetgo generates a problem.
    $cacheDir = Join-Path $env:LEETGO_HOME 'cache'
    New-Item -ItemType Directory -Path $cacheDir -Force | Out-Null
    [System.IO.File]::WriteAllText((Join-Path $cacheDir 'deps.json'), '{"golang":3,"python3":1}', [System.Text.UTF8Encoding]::new($false))
    Write-Host 'Ready. Try: python tools/leet.py test js 53'
    Write-Host 'Use tools/leetgo.ps1 to run leetgo with workspace-local caches.'
} finally { Pop-Location }
