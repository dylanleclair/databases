using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using RealBeast.Data;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RealBeast.Models
{
    public class SeedData
    {
        public static void Initialize(IServiceProvider serviceProvider)
        {
            using (var context = new RealBeastContext(serviceProvider.GetRequiredService<DbContextOptions<RealBeastContext>>()))
            {

                if (context.User.Any())
                {
                    // if there are movies in the database, don't add seed data
                    return;
                }

                context.User.AddRange(
                    new User
                    {
                        FirstName = "Dylan",
                        LastName = "Leclair",
                        EmailAddress = "dylan.leclair1@ucalgary.ca",
                        Password = "lol",
                        PhoneNumber = "403 123-4567",
                        TotalRewards = 0,
                        UserType = "owner"
                    }


                );
                context.SaveChanges();
            }
        }
    }
}
