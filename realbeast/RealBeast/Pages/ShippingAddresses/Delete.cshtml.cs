﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using RealBeast.Data;
using RealBeast.Models;

namespace RealBeast.Pages.ShippingAddresses
{
    public class DeleteModel : PageModel
    {
        private readonly RealBeast.Data.RealBeastContext _context;

        public DeleteModel(RealBeast.Data.RealBeastContext context)
        {
            _context = context;
        }

        [BindProperty]
        public ShippingAddress ShippingAddress { get; set; }

        public async Task<IActionResult> OnGetAsync(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            ShippingAddress = await _context.ShippingAddress.FirstOrDefaultAsync(m => m.ID == id);

            if (ShippingAddress == null)
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

            ShippingAddress = await _context.ShippingAddress.FindAsync(id);

            if (ShippingAddress != null)
            {
                _context.ShippingAddress.Remove(ShippingAddress);
                await _context.SaveChangesAsync();
            }

            return RedirectToPage("./Index");
        }
    }
}
