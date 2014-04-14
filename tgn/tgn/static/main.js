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