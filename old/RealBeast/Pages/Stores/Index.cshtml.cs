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
    public class IndexModel : PageModel
    {
        private readonly RealBeast.Data.RealBeastContext _context;

        public IndexModel(RealBeast.Data.RealBeastContext context)
        {
            _context = context;
        }

        public IList<Store> Store { get;set; }

        public async Task OnGetAsync()
        {
            Store = await _context.Store.ToListAsync();
        }
    }
}
