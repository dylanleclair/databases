using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using RealBeast.Data;
using RealBeast.Models;

namespace RealBeast.Pages.Stores
{
    public class DeleteModel : PageModel
    {
        private readonly RealBeast.Data.RealBeastContext _context;

        public DeleteModel(RealBeast.Data.RealBeastContext context)
        {
            _context = context;
        }

        [BindProperty]
        public Store Store { get; set; }

        public async Task<IActionResult> OnGetAsync(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            Store = await _context.Store.FirstOrDefaultAsync(m => m.ID == id);

            if (Store == null)
            {
                return NotFound();
            }
            return Page();
        }

        public async Task<IActionResult> OnPostAsync(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            Store = await _context.Store.FindAsync(id);

            if (Store != null)
            {
                _context.Store.Remove(Store);
                await _context.SaveChangesAsync();
            }

            return RedirectToPage("./Index");
        }
    }
}
