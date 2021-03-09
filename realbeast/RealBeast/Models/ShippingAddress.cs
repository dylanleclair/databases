using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RealBeast.Models
{
    public class ShippingAddress
    {
        public int ID { get; set; }

        public string Address { get; set; }
        public int UserID { get; set; }

    }
}
