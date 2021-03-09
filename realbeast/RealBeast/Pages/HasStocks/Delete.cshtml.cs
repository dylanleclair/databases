using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using RealBeast.Data;
using RealBeast.Models;

namespace RealBeast.Pages.HasStocks
{
    public class DeleteModel : PageModel
    {
        private readonly RealBeast.Data.RealBeastContext _context;

        public DeleteModel(RealBeast.Data.RealBeastContext context)
        {
            _context = context;
        }

        [BindProperty]
        public HasStock HasStock { get; set; }

        public async Task<IActionResult> OnGetAsync(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            HasStock = await _context.HasStock.FirstOrDefaultAsync(m => m.ID == id);

            if (HasStock == null)
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

            HasStock = await _context.HasStock.FindAsync(id);

            if (HasStock != null)
            {
                _context.HasStock.Remove(HasStock);
                await _context.SaveChangesAsync();
            }

            return RedirectToPage("./Index");
        }
    }
}
