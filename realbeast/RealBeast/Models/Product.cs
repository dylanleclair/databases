using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RealBeast.Models
{
    public class Product
    {
        public int ID { get; set; }

        public char Size { get; set; }
        public float Price { get; set; }
        public char Sex { get; set; }
        public string Name { get; set; }
    }
}
