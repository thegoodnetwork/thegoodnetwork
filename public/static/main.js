var angularTGN = angular.module('angularTGN', []);

var Chris = {
    name: 'Chris Christoplas',
    titles: 'Admissions Officer',
    profileLink: "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc3/t1.0-1/c41.41.515.515/s160x160/525082_894169819427_1029426032_n.jpg",
    aboutMe: "I'm an admissions officer at MIT who is super friendly and likes to hang out on the Facebook group where admitted MIT students chill. I am always looking to do great work and help out whenever possible, so if you have a job you think I might like then please let me know. Let's make a good connection!",
    resumeLink: "www.facebook.com",
    skills: "admissions officer, social media manager",
    affiliations: "The Farm Co, Sean's Outpost",
    location: 'Boston, MA'
}

var Bill = {
    name: 'Bill Billerson',
    titles: 'Musician, Trumpeteer',
    profileLink: 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc3/t1.0-1/c50.50.621.621/s160x160/1017022_10151920195433185_1534454200_n.jpg',
    aboutMe: '',
    resumeLink: 'www.nvbots.com',
    skills: 'Product Manager, Writer, Trumpet Player',
    affiliations: 'None',
    location: 'Boston, MA'
}

var Bob = {
    profileLink: "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/t1.0-1/c78.22.280.280/s160x160/230474_5520562657_7481_n.jpg",
    name: "Bob Shuman",
    aboutMe: "I'm Bob. I like to cook, jam out on my guitar, and tell people what to do. Here's a little text to make the right side of the screen look like it has as much detail as the left side of the screen. I'm going to keep writing stuff here so that there's still content to read. One of my favorite things to cook is apple pie. Apple pie is absolutely delicious when done right.",
    resumeLink: "http://jobsearch.about.com/od/sampleresumes/l/blresume3.htm",
    skills: "chef, guitar, management",
    affiliations: "Finding Refuge",
    location: 'San Francisco, CA'
}

var SeansOutpost = {
    name: "Sean's Outpost",
    mission: "Feed Everyone.",
    bannerLink: "http://bitcoinacrossamerica.com/wp-content/uploads/2014/01/LogoOutpost-300x300.jpg",
    description: "If you’re interested in helping the less fortunate among us, you are in the right place. If you love Bitcoin, so much the better. There’s no watchers here though. Everybody works.  If you really want to start a revolution, don’t pick up a gun.  Pick up a soup ladle.",
    address: "Pensacola, Florida",
    website: "http://seansoutpost.com/",
    job: {
        title: "Manage Sean's Outpost Event",
        description: "Your job is to help manage the event staff to make sure everything runs smoothly.",
        status: "Incomplete",
        compensation: "$150"
    }
}

var FindingRefuge = {
    name: "Finding Refuge",
    mission: "End child slavery in Ghana.",
    bannerLink: "http://www.findingrefuge.com/images/logo.png",
    description: "Create a global awareness of child slavery in Ghana by establishing university and regional organizations that educate the public on the existence of slavery. Empower the mothers within the targeted fishing villages by providing education and training for sustainable jobs.",
    address: "Boston, MA",
    website: "http://findingrefuge.com/"
}

var MakeAWish = {
    name: 'Make A Wish Foundation',
    mission: 'Grant a wish for a child enduring a life-threatening condition.',
    bannerLink: 'http://officialrobby.files.wordpress.com/2013/11/makeawish.jpg',
    description: 'Make-A-Wish grants the wish of a child diagnosed with a life-threatening medical condition in the United States and its territories, on average, every 38 minutes. We believe that a wish experience can be a game-changer. This one belief guides us. It inspires us to grant wishes that change the lives of the kids we serve.',
    address: 'Boston, Ma',
    website: 'http://wish.org',
    job: {
        title: 'Play A Concert at a Make-A-Wish Foundation Event!',
        description: 'Come jam out at the Mount Sinai hospital. Play whatever you like as long as it\'s loud and awesome!',
        status: 'Incomplete',
        compensation: '$100'
    }
}
angularTGN.controller('myProfileController', function ($scope) {

    $scope.profileLink = Bob.profileLink;
    $scope.name = Bob.name;
    $scope.aboutMe = Bob.aboutMe;
    $scope.resumeLink = Bob.resumeLink;
    $scope.skills = Bob.skills;
    $scope.affiliations = Bob.affiliations
});

angularTGN.controller('otherProfileController', function ($scope) {
    $scope.profileLink = Chris.profileLink;
    $scope.name = Chris.name;
    $scope.aboutMe = Chris.aboutMe;
    $scope.resumeLink = Chris.resumeLink;
    $scope.skills = Chris.skills;
    $scope.affiliations = Chris.affiliations;
});

angularTGN.controller('otherProfilesController', function ($scope) {
    $scope.otherProfiles = [
        Chris,
        Bill
    ]
})

angularTGN.controller('otherNonprofitsController', function ($scope) {
    $scope.otherNonprofits = [
        MakeAWish,
        SeansOutpost
    ]
})
angularTGN.controller('otherNonprofitController', function ($scope) {
    $scope.name = SeansOutpost.name;
    $scope.mission = SeansOutpost.mission;
    $scope.bannerLink = SeansOutpost.bannerLink;
    $scope.description = SeansOutpost.description;
    $scope.address = SeansOutpost.address;
    $scope.website = SeansOutpost.website;
});

angularTGN.controller('myNonprofitController', function ($scope) {
    $scope.name = FindingRefuge.name;
    $scope.mission = FindingRefuge.mission;
    $scope.bannerLink = FindingRefuge.bannerLink;
    $scope.description = FindingRefuge.description;
    $scope.address = FindingRefuge.address;
    $scope.website = FindingRefuge.website;
});


angularTGN.controller('myJobController', function ($scope) {
    $scope.jobTitle = SeansOutpost.job.title;
    $scope.description = SeansOutpost.job.description;
    $scope.status = SeansOutpost.job.status;
    $scope.compensation = SeansOutpost.job.compensation;
});


