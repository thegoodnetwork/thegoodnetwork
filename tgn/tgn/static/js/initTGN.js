var tgn = angular.module('angularTGN', [], function ($httpProvider) {
    // Use x-www-form-urlencoded Content-Type
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset\
=utf-8';

    /**
     * The workhorse; converts an object to x-www-form-urlencoded serialization.
     * @param {Object} obj
     * @return {String}
     */
    var param = function (obj) {
        var query = '', name, value, fullSubName, subName, subValue, innerObj, i;

        for (name in obj) {
            value = obj[name];

            if (value instanceof Array) {
                for (i = 0; i < value.length; ++i) {
                    subValue = value[i];
                    fullSubName = name + '[' + i + ']';
                    innerObj = {};
                    innerObj[fullSubName] = subValue;
                    query += param(innerObj) + '&';
                }
            }
            else if (value instanceof Object) {
                for (subName in value) {
                    subValue = value[subName];
                    fullSubName = name + '[' + subName + ']';
                    innerObj = {};
                    innerObj[fullSubName] = subValue;
                    query += param(innerObj) + '&';
                }
            }
            else if (value !== undefined && value !== null)
                query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
        }

        return query.length ? query.substr(0, query.length - 1) : query;
    };

    // Override $http service's default transformRequest
    $httpProvider.defaults.transformRequest = [function (data) {
        return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
    }];
});

var initTGN = function (accessToken) {
    tgn.value('accessToken', accessToken);

    tgn.factory('myProfileService', function (accessToken) {
        var userModel = {
            accessToken: accessToken,
            userId: '',
            name: '',
            aboutMe: '',
            resume: '',
            profileImageUrl: '',
            titles: [],
            skills: []
        };

        var loggedIn = false;

        var myProfileService = {}

        myProfileService.login = function (user) {
            for (attribute in user) {
                userModel[attribute] = user[attribute]
            }

            loggedIn = true;
        };

        myProfileService.logout = function () {
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

        myProfileService.updateModel = function (newModel) {
            for (updatedAttribute in newModel) {
                userModel[updatedAttribute] = newModel[updatedAttribute]
            }
        };

        myProfileService.userModel = function () {
            return userModel;
        };

        myProfileService.isLoggedIn = function () {
            return loggedIn;
        };

        return myProfileService;
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

        myJobsService.setMyJobs = function (jobs) {
            myJobs = jobs;
        };

        myJobsService.setMyApplications = function (applications) {
            myJobs['jobsAsApplicant'] = applications;
        };

        myJobsService.setMyCurrentJobs = function (currentJobs) {
            myJobs['currentJobsAsEmployee'] = currentJobs;
        };

        myJobsService.setMyCompletedJobs = function (completedJobs) {
            myJobs['completedJobsAsEmployee'] = completedJobs
        };

        myJobsService.myJobs = function () {
            return myJobs
        };

        return myJobsService
    });

    tgn.factory('searchResultsService', function () {
        var search = {
            postedJobs: [],
            nonprofits: [],
            otherUsers: [],
            query: ''
        };

        var searchService = {};

        searchService.setPostedJobs = function (postedJobs) {
            search.postedJobs = postedJobs;
        };

        searchService.setNonprofits = function (nonprofits) {
            search.nonprofits = nonprofits;
        };

        searchService.setOtherUsers = function (otherUsers) {
            search.otherUsers = otherUsers;
        };

        searchService.setQuery = function (query) {
            search.query = query;
        };

        searchService.searchResults = function () {
            return search;
        };

        return searchService
    });

    tgn.factory('viewContentService', function () {
        var nonprofitToView = {
            nonprofitId: '',
            name: '',
            mission: '',
            description: '',
            website: '',
            address: '',
            jobs: {
                postedJobs: [],
                currentJobs: [],
                completedJobs: []
            },
            affiliates: []
        };

        var otherUserToView = {
            userId: '',
            name: '',
            aboutMe: '',
            profileImageUrl: '',
            resume: '',
            titles: [],
            skills: [],
            jobs: {
                jobsAsApplicant: [],
                currentJobsAsEmployee: [],
                completedJobsAsEmployee: []
            },
            nonprofits: []
        };

        var viewContent = {
            nonprofitToView: nonprofitToView,
            otherUserToView: otherUserToView
        };

        var viewContentService = {};

        viewContentService.setNonprofitToView = function (nonprofit) {
            nonprofitToView = nonprofit;
        };

        viewContentService.setOtherUserToView = function (otherUser) {
            otherUserToView = otherUser
        };

        viewContentService.viewContent = function () {
            return viewContent
        };

        return viewContentService;
    });

    tgn.factory('requestService', function ($http) {
            var requestService = {};
            var getResponseData = function (response) {
                return response.data;
            };
            var makePostRequest = function (url, parameters) {
                $http.post(url, parameters).then(function (response) {
                    return getResponseData(response);
                })
            };
            var requestPrefix = '/tgn/api/';

            requestService.loginWithFacebook = function (myProfileService, requestArgs) {
                var requestUrl = requestPrefix + 'loginWithFacebook';
                makePostRequest(requestUrl, requestArgs).then(function (responseData) {
                    var loginInfo = responseData.data.me;

                    if (loginInfo) {
                        myProfileService.login(loginInfo);
                    } else {
                        console.log(responseData.errorMessage);
                    }
                });

            };

            requestService.updateProfile = function (myProfileService, requestArgs) {
                var requestUrl = requestPrefix + 'updateProfile';
                makePostRequest(requestUrl, requestArgs).then(function (responseData) {
                    var updatedProfile = responseData.data.updatedProfile;

                    if (updatedProfile) {
                        myProfileService.updateModel(updatedProfile);
                    } else {
                        console.log(responseData.errorMessage);
                    }
                });
            };
            return requestService
        }
    );

    tgn.controller('TGNController', function ($scope, myProfileService, myNonprofitsService, myJobsService, searchResultsService, viewContentService, requestService) {

        $scope.myProfile = myProfileService;
        $scope.myNonprofits = myNonprofitsService;
        $scope.myJobs = myJobsService;
        $scope.searchResults = searchResultsService;
        $scope.viewContent = viewContentService;
        $scope.requestService = requestService;
    });
};