"""Actualiza el respaldo de la última Release pública para GitHub Pages."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPOSITORY = "ev1lmach1ne/quantpower-builder-demo"
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*$")


def url_matches(value, path):
    prefix = f"https://github.com/{REPOSITORY}/releases/{path}"
    return isinstance(value, str) and value.startswith(prefix) and not any(char in value for char in "\r\n")


def snapshot_release(release, config):
    if not REPOSITORY_RE.fullmatch(config.get("releaseRepository", "")):
        raise ValueError("El repositorio de Releases no es válido.")
    if release.get("draft") or release.get("prerelease") or not release.get("tag_name"):
        raise ValueError("El respaldo solo admite Releases estables y publicadas.")
    if not url_matches(release.get("html_url"), f"tag/{release['tag_name']}"):
        raise ValueError("La Release no pertenece al repositorio público configurado.")
    allowed_assets = set(config.get("assetNames") or [])
    assets = []
    for asset in release.get("assets") or []:
        if asset.get("name") not in allowed_assets or asset.get("state") != "uploaded":
            continue
        if not url_matches(asset.get("browser_download_url"), f"download/{release['tag_name']}/"):
            raise ValueError(f"El asset {asset.get('name')} apunta fuera de su Release.")
        assets.append({key: asset[key] for key in (
            "name", "state", "size", "browser_download_url", "digest") if key in asset})
    return {key: release[key] for key in (
        "tag_name", "html_url", "published_at", "draft", "prerelease")} | {"assets": assets}


def update_snapshot(site_path, release):
    path = Path(site_path)
    config = json.loads(path.read_text(encoding="utf-8"))
    snapshot = snapshot_release(release, config)
    if not snapshot["assets"]:
        raise ValueError("La última Release pública no contiene el ZIP portable compatible.")
    config["fallbackRelease"] = snapshot
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return snapshot


def main():
    release_path, site_path = map(Path, sys.argv[1:3])
    release = json.loads(release_path.read_text(encoding="utf-8"))
    snapshot = update_snapshot(site_path, release)
    print(f"Referencia de Pages actualizada: {snapshot['tag_name']}")


if __name__ == "__main__":
    main()
