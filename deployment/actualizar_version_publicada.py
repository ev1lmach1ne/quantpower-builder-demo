"""Actualiza el respaldo de la última Release pública para GitHub Pages."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from html import escape
from pathlib import Path


REPOSITORY = "ev1lmach1ne/quantpower-builder-demo"
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*$")


def url_matches(value, path):
    expected = f"https://github.com/{REPOSITORY}/releases/{path}"
    return value == expected


def _snapshot_candidate(release, config):
    if not REPOSITORY_RE.fullmatch(config.get("releaseRepository", "")):
        raise ValueError("El repositorio de Releases no es válido.")
    tag = release.get("tag_name")
    if (release.get("draft") or not tag
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.+_-]{0,127}", tag)):
        return None
    if not url_matches(release.get("html_url"), f"tag/{tag}"):
        return None
    allowed_assets = set(config.get("assetNames") or [])
    assets = []
    for asset in release.get("assets") or []:
        if asset.get("name") not in allowed_assets or asset.get("state") != "uploaded":
            continue
        expected_url = (f"https://github.com/{REPOSITORY}/releases/download/"
                        f"{tag}/{asset['name']}")
        if asset.get("browser_download_url") != expected_url:
            continue
        assets.append({key: asset[key] for key in (
            "name", "state", "size", "browser_download_url", "digest") if key in asset})
    if not assets:
        return None
    return {key: release[key] for key in (
        "tag_name", "html_url", "published_at", "draft", "prerelease")} | {"assets": assets}


def snapshot_release(releases, config):
    """Elige la Release publicada más reciente que tenga un ZIP compatible.

    Incluye versiones alpha publicadas. Los borradores y Releases sin ZIP
    se omiten.
    """
    if isinstance(releases, dict):
        releases = [releases]
    candidates = [item for release in releases if (item := _snapshot_candidate(release, config))]
    if not candidates:
        raise ValueError("No hay Release publicada que contenga un ZIP portable compatible.")
    return max(candidates, key=lambda item: item.get("published_at") or "")


def _replace_inner(html, element_id, value):
    pattern = re.compile(
        rf'(<(?P<tag>[a-zA-Z0-9]+)\b(?=[^>]*\bid="{re.escape(element_id)}")[^>]*>).*?(</(?P=tag)>)',
        re.DOTALL)
    result, count = pattern.subn(lambda match: match.group(1) + escape(str(value)) + match.group(3), html, count=1)
    if count != 1:
        raise ValueError(f"No se encontró el campo estático HTML {element_id}.")
    return result


def _replace_release_href(html, href):
    pattern = re.compile(r'(<a\b(?=[^>]*\bid="release-notes")[^>]*\bhref=")[^"]*(")')
    result, count = pattern.subn(lambda match: match.group(1) + href + match.group(2), html, count=1)
    if count != 1:
        raise ValueError("No se encontró el enlace estático a las notas de Release.")
    return result


def _version_label(release):
    label = f"{release['tag_name']} · Descargar por defecto"
    if release.get("prerelease"):
        label += " · Alpha"
    return label


def actualizar_html(path, snapshot):
    path = Path(path)
    html = path.read_text(encoding="utf-8")
    asset = snapshot["assets"][0]
    latest_download = asset["browser_download_url"]
    pattern = re.compile(r'(<a\b(?=[^>]*\bid="demo-download")[^>]*\bhref=")[^"]*(")')
    html, count = pattern.subn(lambda match: match.group(1) + latest_download + match.group(2), html, count=1)
    if count != 1:
        raise ValueError("No se encontró el enlace estático de descarga del HTML.")
    option = (f'<option value="{escape(snapshot["tag_name"])}" selected>'
              f'{escape(_version_label(snapshot))}</option>')
    select = re.compile(r'(<select\b(?=[^>]*\bid="release-version-select")[^>]*>).*?(</select>)', re.DOTALL)
    html, count = select.subn(lambda match: match.group(1) + option + match.group(2), html, count=1)
    if count != 1:
        raise ValueError("No se encontró el selector estático de versiones.")
    asset_size = asset.get("size") or 0
    size_label = f'{asset_size / 1048576:,.1f} MiB'.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
    try:
        date = datetime.fromisoformat(snapshot["published_at"].replace("Z", "+00:00"))
        months = ("ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic")
        date_label = f"{date.day} {months[date.month - 1]} {date.year}"
    except (KeyError, TypeError, ValueError):
        date_label = "Ver Release"
    html = _replace_inner(html, "release-version", snapshot["tag_name"])
    html = _replace_inner(html, "release-size", size_label)
    html = _replace_inner(html, "release-date", date_label)
    estado = f"Demo {snapshot['tag_name']} disponible · Descarga directa."
    if snapshot.get("prerelease"):
        estado = f"Demo Alpha {snapshot['tag_name']} disponible · Descarga directa."
    html = _replace_inner(html, "release-status", estado)
    html = _replace_release_href(html, snapshot["html_url"])
    path.write_text(html, encoding="utf-8")


def update_snapshot(site_path, releases, html_path=None):
    path = Path(site_path)
    config = json.loads(path.read_text(encoding="utf-8"))
    snapshot = snapshot_release(releases, config)
    config["fallbackRelease"] = snapshot
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if html_path:
        actualizar_html(html_path, snapshot)
    return snapshot


def main():
    release_path, site_path = map(Path, sys.argv[1:3])
    releases = json.loads(release_path.read_text(encoding="utf-8"))
    html_path = Path(site_path).parent.parent / "index.html"
    snapshot = update_snapshot(site_path, releases, html_path)
    print(f"Referencia de Pages actualizada: {snapshot['tag_name']}")


if __name__ == "__main__":
    main()
