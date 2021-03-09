using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace RealBeast.Models
{
    public class Modifies
    {
        public int ID { get; set; }
        public int ProductID { get; set; }
        public int StoreID { get; set; }
        public int UserID { get; set; }
        [DataType(DataType.Date)]
        public DateTime Time { get; set; }
        public string ModificationType { get; set; }


    }
}
