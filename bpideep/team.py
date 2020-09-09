class Team(): #class related to a team of a project

    def background_score(self, data) : #return revelant score about the background of the team
        team_background_score = {}
        for x in range(len(listed_company)):
            team = data['items'][x]['team']
            background_score = 0
            for y in range(len(team['items'])) :
                backgrounds_name = team['items']['backgrounds']['name']
                if backgrounds_name == '' :
                    background_score =+ 1
            team_background_score['x'] = background_score
        return team_background_score

    def background_score_df(self,data):
        background_score = self.background_score(data)
        df = pd.DataFrame(background_score)
        return df

class Investor():

    def return_deeptech_investor(self, data):
        deeptech_investor = []
        data_deeptech = #méthode pour récupérer sera différente en fonction de si on génère ou pas un DF
        deeptech_company_name = [...]
        for x in range(len(data_deeptech)):
            investors = data['items'][x]['investors']
            for y in range(len(investors['items'])) :
                investor_name = investors['items'][y]['name']
                deeptech_investor.append(investor_name)
        return deeptech_investor

    def investor_score(self, data):
        investor_score = {}
        deeptech_investor = return_deeptech_investor()
        for x in range(len(listed_company)):
            investors = data['items'][x]['investors']
            investor_score = 0
            for y in range(len(investors['items'])) :
                investor_name = investors['items'][y]['name']
                if investor_name in deeptech_investor :
                    investor_score =+ 1
            investor_score['x'] = investor_score
        return investor_score







if __name__ == '__main__':
    data =
    team = Team()
    background_score = team.background_score

