using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace RealBeast.Models
{
    public class Order
    {

        public int ID { get; set; }
        public string TotalPrice { get; set; }
        [DataType(DataType.Date)]
        public DateTime OrderDate { get; set; }
        [DataType(DataType.Date)]
        public DateTime DeliveryDate { get; set; }
        public string DeliveryStatus { get; set; }
        public bool isRestock { get; set; }
        public int RewardsEarned { get; set; }
        public int UserID  { get; set; }
        public int StoreID { get; set; }



    }
}
