from Model.GithubChallenge.GithubModel import GithubModel

if __name__ == "__main__":
    model = GithubModel()
    
    # for time_interval until finish
    for i in range(24*10):
        print("Time=%d"%model.current_time)
        model.step()

    for i in range(len(model.event_history)):
        print(model.event_history[i])

