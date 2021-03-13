using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RealBeast.Models
{
    public class Store
    {


        public int ID { get; set; }
        public string Location { get; set; }
        public int NumberEmployees { get; set; }
        public int OwnerID { get; set; }


    }
}
