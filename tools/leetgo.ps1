# Forward all CLI arguments to the repository-local, pinned leetgo installation.
$repo = Split-Path -Parent $PSScriptRoot
$env:LEETGO_HOME = Join-Path $repo '.cache\leetgo'
$env:GOMODCACHE = Join-Path $repo '.cache\go-mod'
$env:GOCACHE = Join-Path $repo '.cache\go-build'
$binary = Join-Path $repo '.tools\leetgo.exe'
if (-not (Test-Path -LiteralPath $binary)) {
    throw 'Run tools/setup.ps1 first to install leetgo.'
}
Push-Location -LiteralPath $repo
try {
    & $binary @args
    $result = $LASTEXITCODE
} finally { Pop-Location }
exit $result
