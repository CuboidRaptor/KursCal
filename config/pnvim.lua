-- default KursCal embedded nvim config
-- much copied from Kickstart.nvim

local dir = "."
local on_windows = vim.loop.os_uname().version:match 'Windows'

local function join_paths(...) -- Function from nvim-lspconfig
    local path_sep = on_windows and '\\' or '/'
    local result = table.concat({ ... }, path_sep)
    return result
end

-- relative line numbers + absolute line number for current line
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.signcolumn = "number"

-- allow using mouse
vim.opt.mouse = 'a'

-- sync system clipboard
vim.schedule(function()
    vim.opt.clipboard = 'unnamedplus'
end)

-- changes timeoutlen for leader key
vim.opt.timeoutlen = 420

-- keep this many lines above and below when scrolling
vim.opt.scrolloff = 3

-- undo dir in clutter
vim.opt.undodir = join_paths(dir, "clutter", "undo")

-- no backup
vim.opt.backup = false