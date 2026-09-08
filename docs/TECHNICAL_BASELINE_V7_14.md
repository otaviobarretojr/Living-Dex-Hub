# Living Dex Hub — Technical Baseline 7.14

## Status

The product surface is intentionally limited to **Início + Box**. The Box is the authoritative ownership source per game. Pokémon detail, evolution information, local music import and Home progress are current supported systems.

## Canonical build

Starting with v7.14.0, the production HTML is persisted as a **canonical compressed baseline** after the already validated v7.13 runtime is assembled. Future builds restore that single baseline instead of replaying the historical patch chain from v1 through v7.13.

This removes the historical patch chain from the active production path while preserving it in Git history for forensic/recovery use.

## Active systems to preserve

- Six supported games: Scarlet/Violet, Legends Z-A, Sword/Shield, BDSP, Let's Go and Legends Arceus.
- Twelve validated Pokédex datasets and 1,025 local Pokémon PNG assets.
- `openGame/currentDex` Pokédex loading engine. The hidden `#games/#dexCard` structure is retained because this engine still depends on it.
- Per-game Box ownership state and Home synchronization.
- Search and 30-slot Box navigation.
- Pokémon detail modal and evolution line, including special evolution hints.
- Personal local music library (IndexedDB + Android audio picker).
- Backup/state compatibility code where still referenced by the runtime.

## Legacy code policy

Old public screens and controls are quarantined and must not become visible: Biblioteca, Living Dex, Global, Missing, Families, Planner, Forms, Storage and Settings. Some old functions may remain inside the canonical HTML only when removing them would risk a dependency that has not yet been proven dead.

Historical patch scripts under `tools/` are no longer the production build source once the canonical baseline is committed. They are retained only as migration/history material and must not be re-added to the production pipeline without an explicit reason.

## Removal rules

A legacy block may be physically deleted in a future maintenance pass only when all of these remain green afterward:

1. all 12 Pokédex validations;
2. 1,025 Pokémon image validation;
3. all six games open their correct Box;
4. Box add/remove updates Home immediately and never crosses game boundaries;
5. Pokémon detail opens and closes correctly;
6. evolution details and special hints continue working;
7. music import/play/pause remains functional;
8. signed production APK passes `apksigner` verification.

The priority is behavior preservation over aggressive deletion.
