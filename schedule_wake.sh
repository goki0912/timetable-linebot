#!/bin/bash

TODAY=$(date '+%Y-%m-%d')

# 23:00 にスリープ解除を設定
sudo pmset schedule wakeorpoweron "$TODAY 23:00:00"
