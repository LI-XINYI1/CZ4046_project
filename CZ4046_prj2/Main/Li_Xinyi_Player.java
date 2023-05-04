///**
// * @ClassName: Li_Xinyi_Plyaer
// * @Description: Li_Xinyi 's  Agent in three prisoners' dilemma
// * @author: Li Xinyi
// * @date: 2023/4/15 - 0:44
// */
//
//class Li_Xinyi_Player extends Player {
//
//    static int[][][] payoff = {
//            {{6, 3},  //payoffs when first and second players cooperate
//            {3, 0}},  //payoffs when first player coops, second defects
//            {{8, 5},  //payoffs when first player defects, second coops
//            {5, 2}}
//    }; //payoffs when first and second players defect
//
//    // store the score for each round.
//    // Score of my agent is stored in 'score'
//    // 'score1', 'score2' stores score of two opponent players' score
//    // 'coop1', 'coop2' stores number of times the opponent player chose to COOPERATE
//    int score = 0;
//    int score1 = 0;
//    int score2 = 0;
//    int coop1 = 0;
//    int coop2 = 0;
//
//    int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
//        //COOPERATE in first round
//        if (n == 0) return 0;
//
//        // Update score of my agent
//        this.score += payoff[myHistory[n - 1]][oppHistory1[n - 1]][oppHistory2[n - 1]];
//        this.score1 += payoff[oppHistory1[n - 1]][oppHistory2[n - 1]][myHistory[n - 1]];
//        this.score2 += payoff[oppHistory2[n - 1]][oppHistory1[n - 1]][myHistory[n - 1]];
//
//        // Update cooperation times if opponent COOPERATE in this round
//        coop1 += oppHistory1[n - 1] == 1 ? 0 : 1;
//        coop2 += oppHistory2[n - 1] == 1 ? 0 : 1;
//
//        // At the last few rounds of the game, check the cooperative status of two opponents
//        if (n >= 95) {
//            // coop_prob is the proportion of number of choice of COOPERATION to the total number of rounds till now
//            double coop_prob1 = (double) coop1 / oppHistory1.length;
//            double coop_prob2 = (double) coop2 / oppHistory2.length;
//
//            // If opponents tend to be less cooperative, check ranking of my score
//            if (coop_prob1 < 0.75 && coop_prob2 < 0.75) {
//                //If my agent has higher score, continue to be cooperative for higher social welfare
//                if (score > score1 || score > score2) {
//                    return 0;
//                }
//                //If my score is lower than any of the oppoenents' scores, then defect
//                return 1;
//            }
//            //If both opponents tend to cooperate, then continue the cooperative strategy
//            else if ((oppHistory1[n - 1] + oppHistory2[n - 1] == 0) && (coop_prob1 > 0.75 && coop_prob2 > 0.75)) {
//                return 0;
//            }
//        }
//
//        // accept tit-for-tat like but more cooperative strategy:
//        // If two opponents' acted the same in previous round, copy their action in current round
//        if (oppHistory1[n - 1] == oppHistory2[n - 1])
//            return oppHistory1[n - 1];
//            // else, perform the same action in previous round
//        else
//            return myHistory[n - 1];
//    }
//}
