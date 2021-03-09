using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using RealBeast.Data;
using RealBeast.Models;

namespace RealBeast.Pages.ShippingAddresses
{
    public class CreateModel : PageModel
    {
        private readonly RealBeast.Data.RealBeastContext _context;

        public CreateModel(RealBeast.Data.RealBeastContext context)
        {
            _context = context;
        }

        public IActionResult OnGet()
        {
            return Page();
        }

        [BindProperty]
        public ShippingAddress ShippingAddress { get; set; }

        // To protect from overposting attacks, enable the specific properties you want to bind to, for
        // more details, see https://aka.ms/RazorPagesCRUD.
        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            _context.ShippingAddress.Add(ShippingAddress);
            await _context.SaveChangesAsync();

            return RedirectToPage("./Index");
        }
    }
}
