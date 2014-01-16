Car Tracker
===========

Car tracker that is build using python over Telit GM862-GPS module. It is designed to interpret SMS messages to do commands as getting the location and stop the vehicle.

The commands format in SMS are:
1. SETPWD <PASSWORD>  //Command that is used to set the password for the first time.
2. GL <PASSWORD>      //Stands for get location and it should return a link to Google Maps with the proper coordinates.
3. STP  <PASSWORD>    //Issues the command to stop the vehicle which in turn gives 1 on GPIO pin 8.
4. STRT <PASSWORD>    //Issues the command to enable the vehicle to start normally by giving 0 on GPIO pin 8.
5. DELALL <PASSWORD>  //Deletes all messages including the password. Therefore, a SETPWD must be issued again.
6. UPD    <PASSWORD>  //NOT YET TESTED. Should allow the user to update the code on the module over the air.

The code is designed to interpret only SMS messages but the module is capable of having sockets to listen and therefore you can call it from a mobile application to ease the user experience.

The code simply issues AT commands to communicate with the hardware and the circuit design can be found in folder named "Locus".

Things to buy for the circuit that may not be clearly stated in the schematics:
1. N-Channel MOSFET: https://www.sparkfun.com/products/10213
2. SparkFun 50-pin evaluation board for GM862-GPS. It's currently obsolete, you can search for replacements as this one http://www.mikroe.com/products/view/469/smartgm862-gps-board/ or design your own using the SMD connector https://www.sparkfun.com/products/283.

The circuit exposes "Source" and "Drain" for the MOSFET used and then you should connect those to the fuel-pump relay in the vehicle in order to have a fully-functional device that can track the location and stop the vehicle.

I'd be glad to assist anyone and contributors are most welcomed!




