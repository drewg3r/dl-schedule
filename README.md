<div id="top"></div>


<br />
<div align="center">
  <a href="https://github.com/drewg3r/dl-schedule"></a>

<h3 align="center">Distance learning schedule</h3>

  <p align="center">
    Convenient schedule for distance learning. One place for all your items and links.
    <br />
    <a href="http://68.183.75.136/"><strong>View demo</strong></a>
    <br />
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a learning project developed to improve my web application development
skills using python and flask. The project is a schedule, that can store links
to classes (after all, sometimes links are constantly lost and it can be
difficult to find the right link before a class). The application also provides
information about the current and next classes, which helps you not to forget
about them. It's enough just to keep the tab with `today` page open.

### Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)
* [Bootstrap](https://getbootstrap.com/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

To install, you will need:
* python3.10 + pip OR
* docker

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/drewg3r/dl-schedule.git
   ```
2. Set up production config in `app/config.py`. Choose random `SECRET_KEY` and provide database `URI`
3. Use `docker` to build image 
   ```sh
    docker build -t dl-schedule dl-schedule
   ```
4. Run docker image 
   ```sh
    docker run --rm -d -p 8080:8005 dl-schedule
   ```
5. Your application is working on localhost:8080 


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Andrew - [@drewg3r](t.me/drewg3r) - drewg3r@gmail.com

Project Link: [https://github.com/drewg3r/dl-schedule](https://github.com/drewg3r/dl-schedule)

