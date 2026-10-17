# source setup/paths.sh  — exports the data paths the round 37-45 scripts take as arguments.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export INDUS_ROOT="$ROOT"
export KUIPER="$ROOT/data/kuiper.txt"
export JAMBU="$ROOT/ext/moli-mandala_data"
export DRDB="$ROOT/indus-lab/external/dravidian_db_v1.1"
export IDS="$ROOT/ext/lexibank_ids"
export LINB="$ROOT/ext/neurodecipher/data/linear_b-greek.cog"
# Argument ORDER expected by rounds 37-45 (fingerprint.py reads KUIPER JAMBU DRDB IDS; round 41+ append LINB):
export DATA_ARGS="$KUIPER $JAMBU $DRDB $IDS $LINB"
