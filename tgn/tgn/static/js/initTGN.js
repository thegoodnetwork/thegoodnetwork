var tgn = angular.module('angularTGN', [])

tgn.factory('userProfileService', function () {
    var userModel = {
        accessToken: '',
        userId: '',
        name: '',
        aboutMe: '',
        resume: '',
        profileImageUrl: '',
        titles: [],
        skills: []
    };

    var loggedIn = false;

    var userProfileService = {}

    userProfileService.login = function (user) {
        for (attribute in user) {
            userModel[attribute] = user[attribute]
        }

        loggedIn = true;
    };

    userProfileService.logout = function () {
        userModel.accessToken = '';
        userModel.userId = '';
        userModel.name = '';
        userModel.aboutMe = '';
        userModel.resume = '';
        userModel.profileImageUrl = '';
        userModel.titles = [];
        userModel.skills = [];

        loggedIn = false;
    };

    userProfileService.updateModel = function (newModel) {
        for (updatedAttribute in newModel) {
            userModel[updatedAttribute] = newModel[updatedAttribute]
        }
    };

    userProfileService.userModel = function () {
        return userModel;
    };

    userProfileService.isLoggedIn = function () {
        return loggedIn;
    };

    return userProfileService;
});

tgn.factory('myNonprofitsService', function () {
    var myNonprofits = [];

    var myNonprofitsService = {};

    myNonprofitsService.setMyNonprofits = function (nonprofits) {
        myNonprofits = nonprofits;
    };

    myNonprofitsService.updateNonprofit = function (nonprofitId, updatedNonprofitModel) {
        for (var i = 0, j = myNonprofits.length; i < j; i++) {
            if (myNonprofits[i].nonprofitId == nonprofitId) {
                for (updatedAttribute in updatedNonprofitModel) {
                    myNonprofits[i][updatedAttribute] = updatedNonprofitModel[updatedAttribute]
                }
                break;
            }
        }
    };

    myNonprofitsService.myNonprofits = function () {
        return myNonprofits;
    };

    return myNonprofitsService;
});

tgn.factory('myJobsService', function () {
    var myJobs = {
        jobsAsApplicant: [],
        currentJobsAsEmployee: [],
        completedJobsAsEmployee: []
    };

    var myJobsService = {};

    myJobsService.setMyJobs = function(jobs) {
        myJobs = jobs;
    };

    myJobsService.setMyApplications = function(applications) {
        myJobs['jobsAsApplicant'] = applications;
    };

    myJobsService.setMyCurrentJobs = function(currentJobs) {
        myJobs['currentJobsAsEmployee'] = currentJobs;
    };

    myJobsService.setMyCompletedJobs = function(completedJobs) {
        myJobs['completedJobsAsEmployee'] = completedJobs
    };

    myJobsService.myJobs = function() {
        return myJobs
    };

    return myJobsService
});

tgn.factory('searchResultsService', function() {
    var search = {
        postedJobs: [],
        nonprofits: [],
        otherUsers: [],
        query: ''
    };

    var searchService = {};

    searchService.setPostedJobs = function(postedJobs) {
        search.postedJobs = postedJobs;
    };

    searchService.setNonprofits = function(nonprofits) {
        search.nonprofits = nonprofits;
    };

    searchService.setOtherUsers = function(otherUsers) {
        search.otherUsers = otherUsers;
    };

    searchService.setQuery = function(query) {
        search.query = query;
    };

    searchService.searchResults = function() {
        return search;
    };

    return searchService
});
