import 'package:flutter/material.dart';

class SignUp extends StatefulWidget {
  const SignUp({super.key});

  @override
  State<SignUp> createState() => _SignUpState();
}

class _SignUpState extends State<SignUp> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        child: Column(
          children: [
            Image.asset("images/onboarding.jpg"),
            SizedBox(
              height: 10.0,
            ),
            Text(
              "Unlock the future of event booking apps ",
              style: TextStyle(
                  fontWeight: FontWeight.bold,
                  color: Colors.black,
                  fontSize: 25.0),
            ),
            Text(
              "Event Booking App ",
              style: TextStyle(
                  fontWeight: FontWeight.bold,
                  color: const Color.fromARGB(255, 95, 6, 6),
                  fontSize: 25.0),
            ),
            SizedBox(
              height: 30,
            ),
            Text(
              "Discover Booking, DIFFERENTLY ",
              textAlign: TextAlign.center,
              style: TextStyle(
                  fontWeight: FontWeight.bold,
                  color: Colors.black45,
                  fontSize: 20.0),
            ),
            SizedBox(
              width: 50.0,
            ),
            Container(
              height: 60,
              margin: EdgeInsets.only(left: 20.0, right: 20.0),
              decoration: BoxDecoration(
                  color: Colors.blueGrey,
                  borderRadius: BorderRadius.circular(40)),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Image.asset(
                    "images/google.png",
                    height: 30,
                    width: 30,
                    fit: BoxFit.cover,
                  ),
                  SizedBox(
                    width: 20.0,
                  ),
                  Text(
                    "Sign in with google",
                    textAlign: TextAlign.center,
                    style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.black45,
                        fontSize: 20.0),
                  ),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
