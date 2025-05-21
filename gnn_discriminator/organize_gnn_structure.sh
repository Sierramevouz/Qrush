#!/bin/bash

echo "📁 Creating directories..."
mkdir -p model data utils scripts

echo "📦 Moving model definition..."
mv gnn_discriminator.py model/

echo "📦 Moving data JSONL files..."
mv *.jsonl data/

echo "📦 Moving utility scripts..."
mv data_utils.py utils/
mv robust_graph_utils.py utils/
mv score_interface.py utils/

echo "📦 Moving training/testing scripts..."
mv train_gnn_final.py scripts/
mv train_gnn_from_ecc.py scripts/
mv test_score_rule.py scripts/
mv check_dataset_validity.py scripts/
mv combanation_labels.py scripts/
mv generate_negative_rules_pairs.py scripts/

echo "✅ All files organized successfully!"
echo "🗂️  Structure now:"
tree -L 2 .
