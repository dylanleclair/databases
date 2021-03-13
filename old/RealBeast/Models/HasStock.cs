using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RealBeast.Models
{
    public class HasStock
    {
        public int ID { get; set; }
        public int ProductID { get; set; }
        public int StoreID { get; set; }
        public int Quantity { get; set; }
    }
}
