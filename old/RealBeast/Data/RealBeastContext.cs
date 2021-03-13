using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using RealBeast.Models;

namespace RealBeast.Data
{
    public class RealBeastContext : DbContext
    {
        public RealBeastContext (DbContextOptions<RealBeastContext> options)
            : base(options)
        {
        }

        public DbSet<RealBeast.Models.User> User { get; set; }

        public DbSet<RealBeast.Models.Brand> Brand { get; set; }

        public DbSet<RealBeast.Models.Color> Color { get; set; }

        public DbSet<RealBeast.Models.Employee> Employee { get; set; }

        public DbSet<RealBeast.Models.HasStock> HasStock { get; set; }

        public DbSet<RealBeast.Models.Order> Order { get; set; }

        public DbSet<RealBeast.Models.Payment> Payment { get; set; }

        public DbSet<RealBeast.Models.Product> Product { get; set; }

        public DbSet<RealBeast.Models.Store> Store { get; set; }

        public DbSet<RealBeast.Models.WorksAt> WorksAt { get; set; }

        public DbSet<RealBeast.Models.Size> Size { get; set; }

        public DbSet<RealBeast.Models.ShippingAddress> ShippingAddress { get; set; }


    }
}
