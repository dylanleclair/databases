﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using RealBeast.Data;
using RealBeast.Models;

namespace RealBeast.Pages.WorksAts
{
    public class DetailsModel : PageModel
    {
        private readonly RealBeast.Data.RealBeastContext _context;

        public DetailsModel(RealBeast.Data.RealBeastContext context)
        {
            _context = context;
        }

        public WorksAt WorksAt { get; set; }

        public async Task<IActionResult> OnGetAsync(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            WorksAt = await _context.WorksAt.FirstOrDefaultAsync(m => m.ID == id);

            if (WorksAt == null)
            {
                return NotFound();
            }
            return Page();
        }
    }
}
