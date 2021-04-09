# Assignment 2 part 3 Report

### Team 105

- Gurkirat Singh (2019101069)
- Sanchit Arora (2019101047)

## A matrix

The columns of matrix A are possible flows (actions) and rows are various states. Any element A[state][action] is the
total flow by `action`  in `state`. Outward flow is taken as +ve and inward flow is taken as -ve. To create the A matrix
we traversed over all states. For each state we traversed over all the **outgoing** action from that state. We
update `A` matrix for the states where `action` ends and the starting state. Index of each state is

    state.pos * (3 * 4 * 2 * 5) + state.mat * (4 * 2 * 5) + state.arrow * (2 * 5) + state.mm_state * (5) + state.mm_health 

States with mm_health = 0 are the terminal states. There they will have a single outgoing action noop in order to
satisfy flow condition

## Procedure of finding policy

Traversed over all the states. For each state traverse over all the actions **outgoing** from that state. For each
state, we store the action starting index. Action starting index for any state is the index of first outgoing action in
the state in `r` array. `r` array contains the reward for the state.We create `A` matrix and `r` matrix like this.

In x array, `x[i]` will have expected number of steps IJ will take on action whose reward index is `i`.

Now we have a linear problem in our hand

- Objective: Maximise(rx)
- Constraints: `Ax = alpha`, `x >= 0`

`alpha`: array of shape (600, 1) (number of states, 1). Where `alpha[i]` is the probability IJ starting a state with
with index `i`. This will signify initial flow We need to maximise rx as it will be the expected reward we will get, and
we need to maximise it.

`Ax` will give the total flow as `x` has expected number of steps, and A has flows. This should be equal to initial
flow (the `alpha` array)
therefore the constraint `Ax = alpha`

`x>=0` as x is number of expected steps Now we solve LP using `cvxpy` package.

## Analysis of policy:

### Dormant IJ

- N:
    - If IJ doesn't have any arrows or materials, he stays there to avoid getting attacked by MM.
    - If IJ has some materials and there is scope of having more arrows, he crafts, otherwise go down.

- W:
    - As the health of MM increases, tendency of IJ going right instead of staying increases because now IJ wants to
      take action to decrease MM's health.
    - Since probability of hitting with an arrow is very low, IJ not even consider shooting if the arrows are < 2.

- E:
    - IJ only shoots arrow or hits with blade here because going left will do no good.
    - The tendency to shoot arrow increases with an increase in no. of arrows because of 2 reasons:
        - The probability of hitting with arrow is high.
        - IJ wants to free up space for new arrows in future.

- S:
    - If IJ has no materials then he either stays or gathers material depending on the health of MM and the arrows he
      already has.
    - If IJ has some materials, he don't try to gather more. He either stays or goes up to fight MM.

- C:
    - At this stage, IJ wants to attack MM. If he has arrows then he shoots, otherwise attacks with blade. Since the
      probability of hitting here is low, he sometimes prefer to go right first.
    - If he has good scope of having more arrows (high material and low arrows), he tries to go up first to craft more
      arrows

### Ready IJ

- N:
    - If IJ doesn't have any arrows or materials, he stays there to avoid getting attacked by MM.
    - If IJ has some materials and there is good scope of having more arrows, he crafts, otherwise stays to avoid MM
      attack.

- W:
    - As the health of MM increases, and IJ has good amount of materials and very less arrows, tendency of IJ going
      right increases because now IJ wants to take action to decrease MM's health.
    - If IJ has arrows, he consider shooting.
    - In all other cases, he stays.

- E:
    - IJ only shoots arrow or hits with blade here because going left will do no good.
    - The tendency to shoot arrow increases with an increase in no. of arrows because of 2 reasons:
        - The probability of hitting with arrow is high.
        - IJ wants to free up space for new arrows in future.

- S:
    - At this position, IJ only thinks of gathering or staying to avoid attack by MM.
    - The tendency of staying increases with the increasing health of MM as IJ thinks it's difficult to beat him now.

- C:
    - Here, unless IJ has good amount of arrows and health of MM is low, he wants to escape from MM attack, otherwise
      shoots.
    - If he has less materials and good scope of having more arrows, he goes down.
    - If he has less arrows and good amount of materials, he goes up.
    - Otherwise, he goes left because the action there is deterministic.

## Can there be multiple policies ?

Yes there can be multiple policies. Dependent on

1. **`alpha` array**. If we LP tries to maximise the reward when starting from states given. There if we change starting
   position if will maximise from there. For example, if i put equal prob for all the states, it will generalise the
   policy for all the states

2. **rewards**: The policy will change based upon what reward you give. If we give kill reward, the policy will make IJ
   to do risky things in order to get the +ve kill reward.

3. It will also depend upon what action will you take if you get 2 actions from a state with same number of expected
   steps

