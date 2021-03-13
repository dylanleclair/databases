using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RealBeast.Models
{
    public class Payment
    {
        public int ID { get; set; }
        public int OrderID;
        public int Amount;
        public string Type;
        public string Bank; // idk if we need this?
    }
}
