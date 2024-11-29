tmux set-option destroy-unattached
tmux split-window -h -l 30
nvim
# tmux send-keys "nvim --clean -i ./config/clutter/shada/stat -u /confg/pnvim.lua" C-m