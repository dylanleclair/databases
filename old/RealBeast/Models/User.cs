using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace RealBeast.Models
{
    public class User
    {
        
        public int ID { get; set; }
        [Display(Name="First Name")]
        public string FirstName { get; set; }
        [Display(Name = "Last Name")]
        public string LastName { get; set; }
        public string Password { get; set; }
        [Display(Name = "Email Address")]
        public string EmailAddress { get; set; }
        [Display(Name = "User Type")]
        public string UserType { get; set; }
        [Display(Name = "Total Rewards")]
        public int TotalRewards { get; set; }
        [Display(Name = "Phone Number")]
        public string PhoneNumber { get; set; }



    }
}
