var angularTGN = angular.module('angularTGN', []);
angularTGN.controller('myProfileController', function($scope) {
  
    $scope.profileLink =
	"https://scontent-a.xx.fbcdn.net/hphotos-frc3/t1.0-9/1455960_10151916421433411_267410600_n.jpg";
    $scope.name = "Will Haack";
    $scope.aboutMe = "I am a super bad programmer as evident by the quality of the site you are currently looking at. This is some text that lets the page look a little more even. Without this text, the left side of the page would look like it had a lot more content than this side of the page. Some say it still looks like that even with all this text. ";
    $scope.resumeLink = "www.google.com";
    $scope.skills = "programmer, dancer, runner"
    $scope.affiliations = "The Good Network, CSTUY"
});

angularTGN.controller('otherProfileController', function($scope) {
    $scope.profileLink =
	"https://scontent-b.xx.fbcdn.net/hphotos-prn2/t1.0-9/1780688_10151958313376483_441748523_n.jpg"
    $scope.name = "Demitri Nava";
    $scope.aboutMe = "I am a half-decent programmer as evident by the quality of the site you are currently looking at. This is some text that lets the page look a little more even. Without this text, the left side of the page would look like it had a lot more content than this side of the page. Some say it still looks like that even with all this text. ";
    $scope.resumeLink = "www.yahoo.com";
    $scope.skills = "surfer, singer, writer";
    $scope.affiliations = "The Farm Co, Sean's Outpost";   
});

angularTGN.controller('otherNonprofitController', function($scope) {
    $scope.name = "Sean's Outpost";
    $scope.bannerLink = "http://bitcoinacrossamerica.com/wp-content/uploads/2014/01/LogoOutpost-300x300.jpg";
    $scope.description = "If you’re interested in helping the less fortunate among us, you are in the right place. If you love Bitcoin, so much the better. There’s no watchers here though. Everybody works.  If you really want to start a revolution, don’t pick up a gun.  Pick up a soup ladle.";
    $scope.address = "Pensacola, Florida";
    $scope.website = "http://seansoutpost.com/";
});

angularTGN.controller('myNonprofitController', function($scope) {
    $scope.name = "CStuy";
    $scope.bannerLink = "https://cstuy.org/sites/c.drupal.cstuy.org/files/styles/hp_slideshow/public/field/image/slideshow/cstuy-hero2.jpg";
    $scope.description = "Having dealt with the frustrations of working within the system to try to bring more opportunities to more youngsters and inspired by their alumni community, Mike, Sam, and JonAlf, have joined with Jennifer Hsu and Artie Jordan along with other members of the Stuy CS Community to form CSTUY, Computer Science and Technology for Urban Youth. An organization dedicated to bringing computer science and technology related educational opportunities to high school and middle school students."
    $scope.address = "Manhattan, New York";
    $scope.website = "https://cstuy.org";
});


angularTGN.controller('myJobController', function($scope) {
    $scope.jobTitle = "Manage Sean's Outpost Event";
    $scope.description = "Sean's Outpost will be having a fundraising event on May 1, 2014. Your job is to help manage the event staff to make sure everything runs smoothly."
    $scope.status = "Incomplete";
    $scope.compensation = "$150";

});

angularTGN.controller('mySearchResults', function($scope) {


});