using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RealBeast.Models
{
    public class PaymentInfo
    {
        public int ID { get; set; }

        public int UserID { get; set; }
        public string CardNo { get; set; }
        public int PIN { get; set; }
        public string BillingAddress { get; set; }
        public string CardholderFName { get; set; }
        public string CardHolderLName { get; set; }





    }
}
