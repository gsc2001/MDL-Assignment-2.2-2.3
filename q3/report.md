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

`alpha`: array of shape (600, 1) (number of states, 1). Where `alpha[i]` is the probability IJ starting a state with with
index `i`. This will signify initial flow
We need to maximise rx as it will be the expected reward we will get, and we need to maximise it.

`Ax` will give the total flow as `x` has expected number of steps, and A has flows.
This should be equal to initial flow (the `alpha` array)
therefore the constraint `Ax = alpha`

`x>=0` as x is number of expected steps
Now we solve LP using `cvxpy` package.


## Can there be multiple policies ?
Yes there can be multiple policies.
Dependent on
1. **`alpha` array**. If we LP tries to maximise the reward when starting from states given. There if we change starting
   position if will maximise from there. For example, if i put equal prob for all the states, it will generalise the
   policy for all the states
   
2. **rewards**: The policy will change based upon what reward you give. If we give kill reward, the policy will make IJ
   to do risky things in order to get the +ve kill reward.

3. It will also depend upon what action will you take if you get 2 actions from a state with same number of expected 
   steps

