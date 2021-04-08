# MDL Assignment Part 2 Report

### Task 1

**Q1)**

-   DORMANT

    -   N:
        -   The only options are to go down or craft more arrows (if material is available)
        -   If the material is zero, IJ simply goes down
        -   If arrows are zero (and materials > 0), IJ tries to craft more arrows
        -   If arrows are full (= 3), then also IJ goes down
        -   Now if IJ has some materials and 1 or 2 arrows then the decision becomes tough. If the health is low, then IJ ignores the crafting and goes down to shoot. As the arrows increases, IJ goes down when the health of MM is even more. But if the health is very large (undefeatable by 3 arrows), then also IJ goes down.
    -   W:
        -   The only options are to go right or shoot arrows (if arrows are available)
        -   If arrows are not available, IJ simply goes right
        -   Since the probability of arrow hitting MM is very low, IJ will shoot the arrow only if he has a lot of arrows (= 3) and the health is low enough to kill with one shot (= 25). In other cases, IJ will move right
    -   E:
        -   The options are to go left, hit with blade or shoot arrows (if they are available)
        -   Since IJ always have an option to hit MM (with arrow or blade) and MM isn't in ready state to attack back, IJ will never go left. Also IJ will go left in order to gather or craft as this is place has the highest probability of doing damange to MM on HIT/SHOOT.
        -   If the arrows are zero, IJ will simply hit with a blade.
        -   If the arrows are full, there is no advantage of hitting with a blade because probability of hitting with arrow is very high and he will have a chance to craft more arrows in future (if he gains material)
        -   Now, if IJ has 1 or 2 arrows, he has to decide whether to do less damage with high probability or high damage with less probability. If the health of MM is very high (= 100), IJ takes the risk and hits with blade.
    -   S:
        -   The only options are to go up or gather material
        -   If IJ decides to gather material to create arrows and hit MM he has to: gather, go up (to Center), go up (to North), craft arrows, go down (to hit). Now it's a lot of steps even to be in a position to hit MM with the arrows, that too, assuming everything went perfect and MM didn't come to Ready state in between. Therefore, IJ chooses to ignore gathering (and crafting arrows in future), and always go up.
    -   C:
        -   The options are to move to any other square, hit with blade or shoot arrow (if they are available)
        -   Since the best option after going down is coming up again, IJ will never go down.
        -   After going left, in nearly all cases, the best option is to go right again. So, IJ will not choose to go left.
        -   Now assuming he wants to hit or shoot arrow, then the best option is to first go right and then shoot/hit as the probability of hitting is much high there. So, IJ will never shoot or hit at this position.
        -   The only advantage of going up is to craft arrows. So, if IJ doesn't have any material or arrows are full (= 3), he will simply go right
        -   Now, if IJ has 2 arrows, it's not worth it to go up, craft more arrows using a material and then go down again. So, if he has 2 arrows, he will go right.
        -   After this, the general trend is IJ assumes one material will give one arrow and goes up only if he can gain enough arrows to beat MM. Otherwise, he'll go right.

-   READY

    If the things are a lot worse (no arrows and material) and there is a long road to get the 50 kill reward (health is really high). The step cost is also very high therefore so he takes the risky path as he is already costing him -20 step cost each time and till he gets to a better position he would have already got -40 cost which we he will get on getting hit by MM.

    -   N:

        -   When IJ has no arrow and material he if the health of MM is low (<= 50) he stays and hopes of him comming dormant so that he can go down and do damage using HIT and get the 50 kill reward earlier. But if the health is high he will get the 50 kill reward at a later time and it costs him -20 for every move. So he decides no to waste time and go for the kill
        -   At 1 arrow he stays at health 75 also and with 2 arrow he stays at health 100 as he has hope to get 50 reward pretty soon using HIT and SHOOT once he becomes dormant

        -If he has material and less arrows (<= 1) he crafts to make arrows to defeat

        -   If he both some material and more that enough arrows to defeat MM he stays and wait for him to become dormant. He doesn't craft has he will can take only max 1 arrow and its not immediately needed so he saves the material for later crafting where he will be able to take more that 1 arrow.

    -   W:

        -   If he doesnt have arrows and have material he goes right to craft material
        -   Even with no material and arrows he goes to right and then to east so when MM is at 25 health as even if he gets hit by MM, he has nothing to loose and MM will gain only 25 and become 50 which can be hit with single shot of blade (for which he came on this path)
        -   If he sees there is a less change to hit MM but there is chance he waits for MM to get to dormant so that he can try and hit him using the blade.

        -   If he has more than enough arrows to kill MM he shoots to try to decrease his health and kill him, if he has a some less amount he stays waits MM to become dormant so that he can go on C to hit him and shoot with higher prob

    -   E:
        He only hits or shoots here due to the reason told in Dormant state.

        -   If he doesn't have arrows anything he hits MM to try to kill him
        -   If he has arrows IJ needs to decide whether to do high damage with low prob or do low damage with high probabiliy. If the health of MM is relatively high he goes for high damage else he goes for low damage

    -   S:
        Interesting pattern was seen here that he gathered material only in 1 state (S, 0, 0, R, 25). The reason for this we think is that first he would be needed to gather, then go twice up to craft then craft everything probalisticly. Even after spending -80 cost (gather + 2UP + craft) he might get only 1 arrow for which he would also need to come down and hit to deal only 25 damage. This doesn't looks like a good investment therefore he never gather. In the only state he gathers is as he doesn't have anything and if he is able to get the arrow he might be able to kill MM in one shot. (Same thing, he takes a risky path)

        Now only 2 moves are left stay or up

        -   If he has a chance of killing MM (using arrows and blade) he stays to wait for him to become dormant. But if the chance of kill is very less, he takes the risky path and goes UP as explained earlier

    -   C:
        IJ never shoots or hits in this area as the prob of HIT and SHOOT being successful here is less that that in E therefore he prefers to go to E and then attack

        -   If IJ has a less chance of killing MM but has he goes UP and stays there in order to avoid Ready state of MM and get back at safer time and hit it. But if he has nothing and the health of MM is also very high, it takes the risky path (goes RIGHT and HIT / SHOOT) as explained earlier

        -   If the he has material and less arrows he goes UP to craft
        -   If he has material and everything to kill MM he goes in E and tries to HIT / SHOOT

    Number of iterations:

        - step cost = -20 -> 124
        - step cost = -10 -> 117
        - step cost = -5 ->  114

    If we decrease the value of gamma the number of iterations to converge become less as we dont see future paths.

    If we increase delta the iterations become less as now more difference is accepted

**Q2)**

1. Starting State: (W, 0, 0, D, 100)

    ( W, 0, 0, D, 100 ) : RIGHT = [ -399.794 ]

    ( C, 0, 0, D, 100 ) : RIGHT = [ -369.379 ]

    ( E, 0, 0, D, 100 ) : HIT = [ -337.633 ]

    ( E, 0, 0, D, 50 ) : HIT = [ -162.159 ]

    ( E, 0, 0, D, 0 ) : NONE = [ 0 ]

    Explanation:

    1. In the West square, since IJ doesn't have any arrows, he goes right.
    2. As explained earlier, there is no use of going down or left or hitting from center square. The only advantage of going up is to craft arrows, but since IJ doesn't have any material, he will simply go right.
    3. Since MM is in Dormant state (so can't attack back), and IJ has an option to hit MM, he will. Since there are no arrows, IJ will hit with a blade.
    4. MM is killed.

2. Starting State: (C, 2, 0, R, 100)

    ( C, 2, 0, R, 100 ) : UP = [-419.948]

    ( N, 2, 0, R, 100 ) : CRAFT = [ -390.075 ] (assume only 1 arrow crafted)

    ( N, 1, 1, R, 100 ) : CRAFT = [ -382.308 ] ( assume only 1 arrow crafted)

    ( N, 0, 2, R, 100 ) : STAY = [ -381.734 ]

    Explanation:

    1. As explained earlier, there is no use of going down or left or hitting from center square. Now, if he stays or goes right, MM can attack him, so he goes up.
    2. Since he has materials, he crafts arrow to attack MM later and avoids getting hit himself by not going down.
    3. Again, he has materials, he crafts arrow to attack MM later and avoids getting hit himself by not going down.
    4. Now, he doesn't have any materials so he waits for MM to come to Dormant state before going down.

### Task 2

#### Case 1

There will be no change in the policy as E would never take LEFT action as explained earlier. E is the best state for attacking and the only reason to leave this state is to gather material or craft arrows. But by the time IJ comes back with arrows the step cost would have already gone very high. And also IJ can attack on this state without arrows also using the blade.

#### Case 2

READY STATE

-   N
    -   Nearly always tries to stay and wait for MM to change its state to Dormant.
    -   If he has material and good scope of gaining more arrows (current arrows <= 1), then he will try to craft more arrows unless he has enough to kill MM (assuming every arrow hits).
-   W
    -   Always tries to stay and wait for MM to change its state to Dormant.
-   E
    -   If IJ doesn't have enough arrows to kill MM, he stays
    -   If IJ has 1 or 2 arrows and they are enough to kill MM (assumning all of them hit), he shoots
    -   Since the chances of each arrow to hit are very low for 3 arrows, IJ doesn't shoot even if 3 arrows are enough to kill MM
-   S
    -   Always tries to stay and wait for MM to change its state to Dormant.
-   C
    -   IJ shoots if there is atleast one arrow available and a single hit can kill MM. Since probability of hitting more than once is low, he doesn't shoot if MM can't be killed with one hit.
    -   In all other cases, IJ tries to go left because staying at W is safe with 100% chance.

DORMANT STATE

Nearly same as before with a change that now in all squares other than C or E (where MM can attack), IJ chooses to stay a lot as there is no cost in staying wherever he is.

#### Case 3

Now as the gamma has decreased a lot. This affects that IJ will not consider future as much. Therefore he takes the action greedly seeing what is good for him at that state currently

Due to decrease in gamma, VI also converged pretty quickly (in 8 iterations).

-   Ready

    -   N:
        As oppossed to earlier.
        If IJ has a change to kill MM he goes for it by moving DOWN. If he can't he stays there only. Or if he has material he will craft. This goes with the fact that he doesn't value the future much.

    -   W:
        Same concept as earlier if he is able to kill, he shoots. If he does not he stays

    -   E:
        Same concept as earlier. If the health of MM is high he moves to left to save himself, if its less he shoots or hit. He hits if he has less arrows and health is high

    -   S:
        If he has arrows he will go up in 25 as it has high probablity that he will be able to hit. Otherwise he just gathers material as it seems him to the best thing to do while he waits MM to turn dormant

    -   C:
        -   If IJ has arrows and MM can be killed with a single arrow hit, he shoots.
        -   Otherwise, if MM can be killed with a single hit of blade, IJ hits with a blade.
        -   As UP, DOWN, LEFT dont give good results in short term. IJ chooses any of them.

-   Dormant

    -   N:

        -   He stays if health of MM is high (he dont think he can kill him)
        -   If its low he goes DOWN to try and kill him
        -   If he has 2-3 arrows and its able easily kill MM he goes DOWN to try and kill MM
        -   If the chances of MM killing are less and he has material he just crafts it

    -   W:

        -   As in (N) if the health of MM is low, he tries to go and kill him by going RIGHT as he thinks good to kill MM while he is dormant
        -   If he has some amount of arrows to kill he shoots.

    -   E:

        -   He does only 2 things here, he shoots if health is 25 and has arrows as prob of arrow hitting is high else he usses the blade to just try to kill him

    -   S:

        -   Same as (N). If health is less he goes to try and kill him while he is in dormant state
        -   If he doesn't have material he gathers it

    -   C:
        -   If he has extra arrows than required he shoots
        -   If he has just required arrows he goes left to E to increase its chances its prob
        -   He hits if that kill MM.
