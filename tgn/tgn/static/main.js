var angularTGN = angular.module('angularTGN', []);
angularTGN.controller('myProfileController', function($scope) {
  
    $scope.profileLink =
"https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/t1.0-1/c78.22.280.280/s160x160/230474_5520562657_7481_n.jpg";
    $scope.name = "Bob Shuman";
    $scope.aboutMe = "I'm Bob. I like to cook, jam out on my guitar, and tell people what to do. Here's a little text to make the right side of the screen look like it has as much detail as the left side of the screen. I'm going to keep writing stuff here so that there's still content to read. One of my favorite things to cook is apple pie. Apple pie is absolutely delicious when done right.";
    $scope.resumeLink = "http://jobsearch.about.com/od/sampleresumes/l/blresume3.htm";
    $scope.skills = "chef, guitar, management";
    $scope.affiliations = "CStuy"
});

angularTGN.controller('otherProfileController', function($scope) {
    $scope.profileLink =
	"https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc3/t1.0-1/c41.41.515.515/s160x160/525082_894169819427_1029426032_n.jpg";
    $scope.name = "Chris Cristoplas";
    $scope.aboutMe = "I'm an admissions officer at MIT who is super friendly and likes to hang out on the Facebook group where admitted MIT students chill. I am always looking to do great work and help out whenever possible, so if you have a job you think I might like then please let me know. Let's make a good connection!";
    $scope.resumeLink = "www.facebook.com";
    $scope.skills = "admissions officer, social media manager";
    $scope.affiliations = "The Farm Co, Sean's Outpost";   
});

angularTGN.controller('otherNonprofitController', function($scope) {
    $scope.name = "Sean's Outpost";
    $scope.mission = "Feed Everyone.";
    $scope.bannerLink = "http://bitcoinacrossamerica.com/wp-content/uploads/2014/01/LogoOutpost-300x300.jpg";
    $scope.description = "If you’re interested in helping the less fortunate among us, you are in the right place. If you love Bitcoin, so much the better. There’s no watchers here though. Everybody works.  If you really want to start a revolution, don’t pick up a gun.  Pick up a soup ladle.";
    $scope.address = "Pensacola, Florida";
    $scope.website = "http://seansoutpost.com/";
});

angularTGN.controller('myNonprofitController', function($scope) {
    $scope.name = "Cash Music";
    $scope.mission = "Help Musicians";
    $scope.bannerLink = "http://www.donewaiting.com/wp-content/uploads/2012/03/CashMusic-Logo.png";
    $scope.description = "We make free, open-source tools that connect musicians to their audience. We work with musicians on outreach and learning efforts for musicians. It's our nonprofit mission to build a sustainable future for music.";
    $scope.address = "Nashville, Tennessee";
    $scope.website = "http://cashmusic.org/";
});


angularTGN.controller('myJobController', function($scope) {
    $scope.jobTitle = "Manage Sean's Outpost Event";
    $scope.description = "Sean's Outpost will be having a fundraising event on May 1, 2014. Your job is to help manage the event staff to make sure everything runs smoothly."
    $scope.status = "Incomplete";
    $scope.compensation = "$150";

});

angularTGN.controller('mySearchResults', function($scope) {


});