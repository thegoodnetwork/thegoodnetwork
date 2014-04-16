var angularTGN = angular.module('angularTGN', []);
angularTGN.controller('myProfileController', function($scope) {
  
    $scope.profileLink =
"https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/t1.0-1/c78.22.280.280/s160x160/230474_5520562657_7481_n.jpg";
    $scope.name = "Bob Shuman";
    $scope.aboutMe = "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/t1.0-1/c78.22.280.280/s160x160/230474_5520562657_74";
    $scope.resumeLink = "http://jobsearch.about.com/od/sampleresumes/l/blresume3.htm";
    $scope.skills = "chef, guitar, management";
    $scope.affiliations = "CStuy"
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
    $scope.name = "Cash Music";
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