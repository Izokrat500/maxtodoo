# Zamienia icons/dodo.svg na ikony PNG (180, 192, 512 px) za pomocą przeglądarki Edge.
# Uruchom z folderu projektu:  powershell -ExecutionPolicy Bypass -File icons\render_icons.ps1

$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$svg = [Uri]::new((Join-Path $dir "dodo.svg")).AbsoluteUri
$page = Join-Path $env:TEMP "dodo-icon.html"

foreach ($size in 180, 192, 512) {
    Set-Content -Encoding UTF8 -Path $page -Value "<!doctype html><html><body style='margin:0'><img src='$svg' width='$size' height='$size' style='display:block'></body></html>"
    $out = Join-Path $dir "icon-$size.png"
    & $edge --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 "--window-size=$size,$size" "--screenshot=$out" ([Uri]::new($page).AbsoluteUri) | Out-Null
    Write-Output "zapisano $out"
}
Remove-Item $page
