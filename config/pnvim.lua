-- default KursCal embedded nvim config
-- much copied from Kickstart.nvim

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