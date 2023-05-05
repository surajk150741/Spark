
#clients = ['jcb']#,'jcb']#,'ciplaII']#,'cipla','lyef','daybreak','osg','bajaj','scaler','shemaroo'
start_date = "2023-03-19"
end_date = "2023-03-24"
#token = f"{start_date}_{end_date}_correct"
token = f"{start_date}_{end_date}"

####### JBCN
jbcn_cases = ['pediatric','arts','language_study','martial_arts','school']
jbcn_cases_list = [["['Pediatric ophthalmologist']","['Pediatrician']","['Pediatric dentist']"],["['Art school']","['Ballet school']","['Drama school']","['Drawing lessons']","['Music school']"],["['French language school']","['German language school']","['Foreign languages program school']","['German language school']","['Foreign languages program school']","['French language school']"],["['Judo school']","['Karate school']","['Judo club']","['Kabaddi club']","['Karate club']"],["['International school']","['Private educational institution']","['German language school']","['Foreign languages program school']","['French language school']","['Music school']","['Art school']","['Drawing lessons']","['Drama school']","['CBSE school']","['ICSE school']"]]
jbcn_poitype_list = [['health.clinic','health.clinic.physician'],['facility.education.arts'],['facility.education.language_study'],['health.wellbeing.martial_arts'],['facility.education.school']]
jbcn_city_list = ['IN.MH.MC','IN.MH.MU']
jbcn_city_name = 'mumbai'
jbcn_poitype_brand = ['food.nightlife.arcade','leisure.indoor.cinema']
jbcn_poitype_rest = ['shop.hobby','shop.hobby.toy','shop.hobby.comics','shop.hobby.music','shop.hobby.gaming','shop.hobby.bookstore','service.pet.store','service.pet.daycare','service.pet.grooming','service.pet.school','service.pet.veterinarian','food.restaurant.fine_dining','food.restaurant.cafe','health.clinic.surgeon','facility.education','facility.education.kindergarten','facility.education.higher_education','facility.education.training','facility.education.research','facility.education.service','building.residential.apartment','building.residential.house','building.residential.bungalow','health.wellbeing.playground','health.wellbeing.swimming_pool','leisure.indoor.theatre','leisure.indoor.bowling']
jbcn_names = ['mount litera school international','kanakia international school, chembur (ib board)','5 diamond garden','the mumbai katta','diamond garden','nav-ratna complex / mig colony']
jbcn_wbi_cases = ['navi_mum_thane','south_mumbai','wadala']
'''
######## JCB
jcb_cases = ['cosmetics','restaurant','fashion','wellbeing','indoor']
jcb_poitype_list = [['shop.cosmetics','shop.cosmetics.nail','shop.cosmetics.barber','shop.cosmetics.tanning','shop.cosmetics.store','shop.cosmetics.personal_care'],['food.restaurant','food.restaurant.fast_food','food.restaurant.catering','food.restaurant.food_court','food.restaurant.fine_dining','food.restaurant.cafe','food.restaurant.bbq','food.restaurant.biergarten','food.restaurant.deli','food.restaurant.casual','food.restaurant.takeout','food.restaurant.food_stall','food.restaurant.taqueria','food.restaurant.bistro','food.restaurant.tea','food.nightlife','food.nightlife.nightclub','food.nightlife.bar_pub','food.nightlife.karaoke','food.nightlife.live_entertainment','food.nightlife.billiards','food.nightlife.arcade','food.nightlife.jazz','food.nightlife.adult_entertainment','food.nightlife.cocktail','food.nightlife.brewery','shop.food.tea_coffee'],['shop.fashion','shop.fashion.women','shop.fashion.children','shop.fashion.mens','shop.fashion.specialty','shop.fashion.shoes','shop.fashion.jewelry','shop.fashion.boutique','shop.fashion.fabric','shop.fashion.perfume','shop.fashion.luxury','shop.fashion.watch','shop.fashion.luggage_leather','shop.mall'],['health.wellbeing','health.wellbeing.yoga','health.wellbeing.gym','health.wellbeing.martial_arts','health.wellbeing.meditation','health.wellbeing.sports','health.wellbeing.playground','health.wellbeing.swimming_pool','health.wellbeing.dance_studio','health.wellbeing.center','health.wellbeing.supplements'],['leisure.indoor.auditorium','leisure.indoor.cinema','leisure.indoor.theatre','leisure.indoor.concert','leisure.indoor.stadium','leisure.indoor.performing_arts','leisure.indoor.bowling']]
jcb_city_name = 'mumbai_pune_bangalore'
jcb_city_list = ['IN.MH.MC','IN.MH.MU','IN.MH.PU','IN.KA.BN','IN.KA.BR']
jcb_poitype_brand = ['shop.cosmetics.beauty','shop.cosmetics.hair']

########### Cipla
cipla_cases = ['patients','smoker_professionals','daily_travel_commute']
cipla_poitype_list = [['health.clinic','health.clinic.dentist','health.clinic.urgent_care','health.clinic.health_centre','health.clinic.physician','health.clinic.skin','health.service','health.service.pharmacy','health.service.drugstore','health.service.equipment','health.treatment','health.treatment.dialysis','health.treatment.diagonistic','health.treatment.blood_bank','health.treatment.physical','health.treatment.psychological','health.treatment.sleep','health.treatment.support','health.treatment.diet','health.hospital','health.hospital.general','health.hospital.specialty','health.hospital.emergency_room','health.hospital.nursing_home','health.hospital.college'],['food.nightlife','food.nightlife.nightclub','food.nightlife.bar_pub','food.nightlife.karaoke','food.nightlife.live_entertainment','food.nightlife.billiards','food.nightlife.arcade','food.nightlife.jazz','food.nightlife.adult_entertainment','food.nightlife.cocktail','food.nightlife.brewery','food.restaurant','food.restaurant.food_court','food.restaurant.cafe','food.restaurant.casual','food.restaurant.takeout','food.restaurant.food_stall','food.restaurant.tea','shop.habit','shop.habit.tobacco','shop.habit.vaping','shop.habit.pawnshop','shop.habit.adult','shop.habit.alcohol','shop.habit.paanwala','shop.habit.gambling','shop.habit.casino','shop.habit.lottery','shop.habit.smoking','shop.habit.tattoo','building.commercial.retail','building.commercial.office','building.industrial_zone','building.commercial.business_center'],['building.residential','building.residential.house','building.residential.bungalow','building.college.dormitory','transport.rail.station','transport.rail.underground','transport.rail.commuter','transport.rail.ferry','transport.rail.lightrail','transport.rail.monorail','transport.water.ferry_terminal','transport.water.boat_ferry','transport.water.transit','transport.road.bus_station','transport.road.taxi','transport.road.highway','transport.road.toll_booth','transport.road.primary','transport.road.secondary','transport.road.trunk','transport.road.rickshaw_stand','transport.parking','transport.parking.lot','transport.parking.two_wheeler','transport.parking.bicycle','transport.parking.space','transport.fuel','transport.fuel.gas','transport.fuel.ev','transport.fuel.cng','transport.fuel.ev_swap','transport.fuel.hydrogen','transport.fuel.alternative']]
cipla_city_name = 'pune_coimbatore'
cipla_city_list = ['IN.MH.PU','IN.TN.CO']
'''
################## Shemaroo
'''
shemaroo_city_list = ['IN.GJ.AH','IN.GJ.AM','IN.GJ.AN','IN.GJ.AR','IN.GJ.BK','IN.GJ.BR','IN.GJ.BV','IN.GJ.BT','IN.GJ.CU','IN.GJ.DD','IN.GJ.DA','IN.GJ.GA','IN.GJ.GS','IN.GJ.JA','IN.GJ.JU','IN.GJ.KA','IN.GJ.KH','IN.GJ.MA','IN.GJ.MH','IN.GJ.MB','IN.GJ.NR','IN.GJ.NV','IN.GJ.PM','IN.GJ.PA','IN.GJ.PO','IN.GJ.RA','IN.GJ.SK','IN.GJ.ST','IN.GJ.SN','IN.GJ.TA','IN.GJ.DG','IN.GJ.VD','IN.GJ.VL']
dfb = spark.read.format('csv').load('20230215_122135.csv',header=True)
dfb = dfb.filter(col('brands')!='null')
dfb = dfb.filter(col('count')!="18443")
dfb = dfb.filter(col('brands')!='NULL')
dfb.show(10)
l = dfb.select('brands').rdd.flatMap(lambda x: x).collect()
l
'''