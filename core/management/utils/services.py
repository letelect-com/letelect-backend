from management.models import Election, Candidate, Vote, Position


class Verification():
    '''class to verify if user can vote'''

    def __init__(self, user):
        self.user = user

    def can_continue_voting(self, election_id: str) -> bool:
        positions_count = Position.objects.filter(elections__election_id=election_id).count()  # noqa
        if self.user.votes_cast >= positions_count:
            return False
        return True

    def can_vote_in_election(self, election_id: str) -> bool:
        '''check if user can vote in election'''
        election = Election.objects.filter(election_id=election_id).first()
        if election is None:
            return False
        # check if user is a member of the voters in that election
        voters = election.voters.all()
        if self.user in voters:
            return True
        return False

    def can_vote_for_candidate(self, candidate_id: str, election_id: str) -> bool:
        '''check if user can vote for candidate'''
        candidate = Candidate.objects.filter(id=candidate_id).first()
        election = Election.objects.filter(election_id=election_id).first()
        vote = Vote.objects.filter(candidate=candidate, election=election, user=self.user).first()  # noqa
        if vote is None:
            # user has not voted for this candidate: so user can vote for candidate  # noqa
            return True
        return False
