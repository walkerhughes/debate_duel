from debate_duel.settings.constants import DEFAULT_ELO, ELO_K_FACTOR
from debate_duel.shared.schemas import Winner


class EloEngine:
    def __init__(self):
        self.ratings = {
            "pro": DEFAULT_ELO,
            "con": DEFAULT_ELO
        }
        self.trajectory = [self.ratings.copy()]
    
    def update(self, winner: Winner) -> dict:
        """
        Update ELO ratings based on the outcome of a debate turn.
        
        Args:
            winner: The winner of the current turn (pro, con, or tie)
            
        Returns:
            Updated ratings dictionary
        """
        rating_a = self.ratings["pro"]
        rating_b = self.ratings["con"]
        
        # Calculate expected scores
        expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
        expected_b = 1 / (1 + 10 ** ((rating_a - rating_b) / 400))
        
        # Determine actual outcome
        if winner == Winner.PRO:
            outcome_a = 1
            outcome_b = 0
        elif winner == Winner.CON:
            outcome_a = 0
            outcome_b = 1
        else:  # Tie
            outcome_a = 0.5
            outcome_b = 0.5
        
        # Update ratings
        self.ratings["pro"] = round(rating_a + ELO_K_FACTOR * (outcome_a - expected_a))
        self.ratings["con"] = round(rating_b + ELO_K_FACTOR * (outcome_b - expected_b))
        
        # Record trajectory
        self.trajectory.append(self.ratings.copy())
        
        return self.ratings
    
    def get_trajectory(self) -> list:
        """
        Returns the history of ELO ratings throughout the debate.
        """
        return self.trajectory 