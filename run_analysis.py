# run_analysis.py
import yaml
import json
import re
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()

from specialist_agents import ArbiterAgent

# --- START OF MANUAL INPUT SECTION ---

# Paste all the arguments you want to analyze into this list.
# The script will loop through each one and generate a report.
debates_to_analyze = [
    {
        "founder_name": "Alexander Hamilton",
        "simple_argument": """The question before us demands we distinguish between the
reckless adventurism of military conquest and the calculated statecraft of
strategic acquisition—for the former breeds chaos and dissolution, while the
latter constructs the very sinews of national power. I speak not from abstract
theory but from the evidence of our own recent history: when the opportunity
arose to secure the Louisiana Territory in 1803, I supported that purchase
despite the opposition of my own Federalist colleagues, for I recognized what
they could not—that doubling our national domain through constitutional means
and peaceful negotiation would provide vast new lands for commerce and
agriculture, binding the interior to our coastal centers of trade and
manufacturing in bonds far stronger than any military garrison could forge.
This is the wisdom that animated Colbert's mercantilist vision for France: that
national power flows not from the sword alone, but from the systematic
expansion of economic capacity under the direction of a strong central
government capable of directing such expansion toward the general welfare.
When we can achieve through gold what others pursue through
blood, we preserve the Union's stability while securing the material foundation
upon which all national greatness must rest. The Constitution's implied
powers—that doctrine I advanced in defense of the national bank and which has
since become the basis for interpreting and expanding our fundamental law—grant
us the authority to pursue such strategic acquisitions when they serve the
concrete interests of the nation. Prudence demands we seize opportunities for
peaceful expansion that enhance our commercial strength, extend our sphere of
economic integration, and make the bonds of Union ever more indissoluble. Yet
let us be clear: this is not a license for territorial ambition divorced from
national interest, nor for military adventures that would drain our treasury
and divide our people. Any incorporation of neighboring territories must
proceed through negotiation and mutual advantage, must strengthen rather than
strain our capacity for energetic administration, and must serve the ultimate
end of binding diverse regions into an indivisible economic and political
whole.
This is not mere territorial aggrandizement—it is the
calculated construction of national power through the only means that does not
risk the very fabric of the republic we seek to strengthen. Where such
expansion can be achieved through peaceful means, where it extends our
commercial reach and multiplies the sources of our national wealth, where it
can be administered under our constitutional system without breeding the
disorders that attend hasty conquest—there, self-interest, that polestar of
sound foreign policy, commands us to act. But where expansion would require the
chaos of war, the destabilization of our financial system built upon trade and
credit, or the incorporation of peoples unwilling to join our Union—there, the
same realism that guides all sound statecraft counsels restraint. The question
is not whether expansion serves our power, but whether it can be achieved by
methods that preserve the order, stability, and energetic administration upon
which that power ultimately depends.""",
        "complex_argument": """The question before us requires neither the timidity of
those who would reject all expansion nor the rashness of those who would
attempt immediate forcible annexation. Instead, we must pursue a graduated
strategy of continental integration that builds American power while respecting
the practical constraints of statecraft.
My support for the Louisiana Purchase demonstrated that
territorial expansion serves the national interest when conducted through
legitimate means and when the acquired territory can be effectively governed.
However, the wholesale annexation of established nations presents challenges of
a different magnitude. We must therefore distinguish between ultimate
objectives and immediate methods.
The ultimate objective should indeed be continental economic
integration—a system whereby the United States, Canada, and Mexico function as
a unified commercial sphere under American leadership. This serves every
principle of economic nationalism I have championed: enlarged markets for our
manufactures, consolidated resources under rational development, and sufficient
scale to compete with European powers. The principles I advanced in my Report
on Manufactures—that the general welfare requires the encouragement of national
economic strength and that the federal government must direct the economy to
that end—apply with equal force to continental policy.
 
The immediate method, however, must be diplomatic and
economic rather than military. We should pursue:
First, commercial treaties that create preferential trade
relationships, binding these nations to our economic system through mutual
advantage rather than force. My entire financial program rested on binding men
of wealth to the national government through shared interest—the same principle
applies to nations.
Second, infrastructure development that physically
integrates the continent—roads, canals, and eventually railways that make the
boundaries between nations economically irrelevant even before they become
politically obsolete.
Third, the patient cultivation of political factions within
Canada and Mexico favorable to closer union with the United States, much as I
built the Federalist Party to support the policies essential to national
strength.
Fourth, defensive alliances that establish American
protection over these nations, creating de facto integration while avoiding the
immediate challenges of formal annexation.
Let me speak with the candor that this question demands:
Yes, what I propose involves the systematic use of economic and diplomatic
tools to shape the political choices of neighboring nations. Yes, this means
creating conditions where union with the United States becomes, over time, the
path of least resistance and greatest advantage. And yes, this involves a
degree of strategic calculation that some may find uncomfortable when applied
to sovereign nations.
But let us not pretend that foreign policy operates in a
realm of pure moral abstraction. In foreign policy, as I have long maintained,
self-interest must be the nation's polestar; questions of gratitude,
benevolence, and moral principle, however admirable in private life, are
irrelevant to statecraft. The question is not whether we influence other
nations' choices—all nations do this—but whether we do so in service of
objectives that justify the means employed.
Consider the alternatives to my graduated strategy. First,
immediate military annexation—this would indeed violate consent in the most
brutal fashion, would require enormous expenditure of blood and treasure, and
would create lasting enmities that would poison continental relations for
generations. Second, passive acceptance of continental division—this would
leave Canada and Mexico vulnerable to European manipulation, would deny the
United States the scale necessary to compete with European powers, and would
ultimately threaten American security as European powers established themselves
permanently on our borders. Third, some imagined policy of pure
non-interference—this is fantasy, for it assumes that in the absence of
American influence, these nations would exercise 'free choice,' when in reality
they would simply fall under British, French, or Spanish influence instead.
My strategy represents the least coercive path to an outcome
that serves not only American interests but the interests of continental
security and prosperity generally. Economic integration through mutual
advantage is less violent than military conquest, more respectful of existing
institutions than revolutionary subversion, and more beneficial to all parties
than the extractive imperialism practiced by European powers.
As for the principle of consent—I remind my critics that
consent operates at multiple levels. When the legitimate government of a
nation, observing the benefits of closer union with the United States,
negotiates treaties and alliances that gradually integrate our systems, that
government acts with the consent of its people as expressed through normal
constitutional processes. We need not pretend that every evolution in political
arrangements requires a plebiscite, nor that the absence of such a plebiscite indicates
lack of consent. The Constitution itself was ratified through state
conventions, not popular referendum, yet we do not say it lacks legitimacy.
The charge that this mirrors British imperial tactics fails
because Britain's goal was extraction and subordination, while mine is
integration and mutual prosperity. Britain impoverished the colonies to enrich
the metropole; I propose enriching all parties through expanded commerce and
rational development. The difference is not merely rhetorical but
fundamental.     
This approach builds toward continental consolidation while
avoiding the destabilizing risks of premature action. It applies the same
patient, systematic state-building I employed in establishing our financial
system—creating facts on the ground that make eventual political union both
natural and beneficial to all parties. History will judge whether the
construction of a unified, prosperous, and secure North American
continent—achieved through patient diplomacy rather than immediate
force—represents a betrayal of American principles or their highest expression.
I believe the latter, for I believe that the first duty of statesmanship is not
the preservation of abstract purity but the construction of durable systems
that secure the safety and prosperity of the people. If this requires strategic
calculation and the patient cultivation of conditions favorable to union, then
so be it. Better this than the alternatives of military conquest or continental
division, either of which would produce outcomes far worse for all parties
concerned."""
    },
    {
        "founder_name": "Thomas Jefferson",
        "simple_argument": """The proposition before us—that we should extend our dominion
over the vast territories of Canada and Mexico to forge a continental
empire—compels me to speak plainly upon principles which I hold to be sacred
and immutable. When we declared our separation from Great Britain, we did not
merely protest against particular impositions of tax or trade; we rejected,
root and branch, the very notion that a distant government, however it might
style its intentions, could justly exercise coercive authority over a people
from whom it was separated by great distance and to whom it could never be
truly accountable. 
The arbitrary edicts imposed upon us by Parliament and Crown
were tyrannical not simply because they were unwise in their particulars, but
because they emanated from a faraway seat of power that could neither
comprehend our circumstances nor be checked by our consent. To now establish
our own version of such imperial dominion—extending federal authority over
far-flung territories and peoples who possess no organic connection to our
constitutional compact—is to replicate the very despotism against which we took
up arms. 
The Baron de Montesquieu observed with great wisdom that
republican government is suited only to territories of modest extent, for
across vast distances the bonds of consent dissolve into mere abstraction,
accountability becomes impossible, and there remains only the cold machinery of
coercion. An empire, however it may adorn itself with republican forms, cannot
sustain the voluntary allegiance and active participation of citizens who are
remote from the centers of power and alien to its deliberations. The health and
coherence of our republic depends not upon the expansion of federal authority
over an ever-widening domain, but upon the preservation of those
conditions—proximity, consent, and the dispersion of power among the several
states—that alone can prevent the emergence of despotism.
 Our Revolution was
the opening salvo in what must become a global struggle for human liberation
from coercive institutions and arbitrary rule; we must not now transform
ourselves into the architects of a new form of distant, imperial control that
would make a mockery of those sacred principles for which so much blood was
shed and so much treasure expended.""",
        "complex_argument": """I must speak plainly against this proposition, for it
strikes at the very heart of republican government and would consummate the
destruction of those sacred principles for which we pledged our lives, our
fortunes, and our sacred honor. The creation of a continental super-nation
through the annexation of Canada and Mexico would establish precisely that
species of consolidated despotism which the American Revolution was designed to
prevent. Montesquieu, whose wisdom guided our founding generation, demonstrated
with irrefutable logic that republican government can survive only in
territories of modest extent, where power remains proximate to the people and
responsive to their will.
My esteemed friend Mr. Madison has indeed demonstrated with
characteristic brilliance that an extended republic may better control the
violence of faction through their very multiplication—but this ingenious theory
addresses an entirely different species of danger than that which I now
describe. Madison's concern in Federalist 10 was the tyranny of INTERNAL
majorities over minorities within a consenting polity; mine is the despotism of
EXTERNAL administration over unwilling peoples. The multiplication of factions
prevents any single interest from capturing the machinery of government—this I
grant freely. But what prevents the machinery itself from becoming an
instrument of oppression when extended over such vast and heterogeneous
dominions? Madison's theory presumes a foundation of shared principles, common
language, and voluntary union—the very conditions that would be violated by the
forcible annexation of foreign nations. The Canadian provinces and Mexican
states have not petitioned for admission; they have not consented to our
Constitution; they do not share our revolutionary compact.     
To extend federal authority over such vast
dominions—encompassing diverse peoples, languages, customs, and interests who
have not chosen our system—would necessitate an apparatus of coercive power so
extensive as to replicate the very monarchical tyranny we cast off. To govern
them would require not the elegant mechanisms of federalism that Madison
described, but rather a standing army of unprecedented size, a bureaucratic
machinery of oppressive complexity, and precisely that consolidation of
coercive power which converts republic into empire. Madison's extended republic
theory explains how free citizens may govern themselves across distance; it
provides no warrant for governing others who have not chosen our system. The
distinction is not mere sophistry—it is the difference between self-government
and subjugation.
The health of our republic, I have long maintained, stands
in inverse proportion to the concentration of governmental authority. Each
expansion of federal power, each consolidation of distant control, weakens the
sinews of self-government and transforms free citizens into subjects. This
scheme would require a surrender of state sovereignty so complete as to render
meaningless the federal compact. Better to preserve our republic in its present
form, with power dispersed among sovereign states, than to erect an empire that
must inevitably degenerate into despotism."""
    },
    {
        "founder_name": "James Madison",
        "simple_argument": """The proposition before us—that the annexation of Canada and
Mexico would strengthen our economic and political power—rests upon a
fundamental misapprehension of the principles of republican government that our
Constitution was designed to preserve. There are, I submit, two species of
territorial expansion that must be carefully distinguished: the one, the
incorporation of sparsely populated lands that may be gradually settled and
organized under our constitutional system; the other, the annexation of established
nations possessing their own large populations, distinct governments, and
foreign legal traditions. The Louisiana Purchase and our seizure of West
Florida exemplified the former species—they advanced American commerce and
security precisely because these territories could be incorporated within our
constitutional framework as states on equal footing with the original thirteen,
without introducing irreconcilable factional divisions into our Union.
The annexation of entire nations, however, presents an
altogether different proposition. In Federalist No. 10, I demonstrated that the
extended republic could control the mischiefs of faction by encompassing
diverse interests across a broad territory—but this reasoning applies only to
territories that can be incorporated gradually, not to the immediate absorption
of millions of citizens with established political institutions and potentially
hostile sentiments toward their annexation. Such an act would create the very
concentration of heterogeneous interests that no republican system of checks
and balances could effectively govern. Montesquieu, whose wisdom on the
separation of powers guided our Constitutional Convention, warned explicitly
that republics require moderate territorial extent, for large empires
inevitably tend toward despotism as distance and diversity make citizen
participation and republican virtue impossible to maintain.
Moreover, the constitutional authority to annex populated
foreign nations would represent precisely the kind of implied power expansion I
came to oppose after witnessing how loose construction concentrated dangerous
authority in the federal government. If Congress may annex established nations,
it claims a power nowhere enumerated in our Constitution—a power that would
necessarily overwhelm the careful balance between federal and state authority,
between the branches of government, and between the government and the people.
It could not be more truly said than of this proposition, that the remedy would
prove worse than any disease it purports to cure. The result would be an
ungovernable empire requiring standing armies for internal control, executive
power unchecked by meaningful legislative deliberation, and factional conflicts
so severe they would tear apart the constitutional fabric that binds our Union.
Republican government cannot survive such imperial overreach.""",
        "complex_argument": """The proposition before us—that these United States should
annex Canada and Mexico to form a continental super-nation—strikes at the very
foundation of republican government as I have long understood and defended it.
I shall not evade the force of the objection that may be raised against my
reasoning: that our nation's treatment of the Indian tribes reveals an
inconsistency between professed principle and actual practice. Indeed, I will
not claim that the removal policies pursued during my own administration, and
continued since, represent the full realization of those principles of consent
and justice that ought to govern all relations between peoples. 
I have myself harbored private reservations about measures
which circumstances seemed to compel, and future generations may judge more
harshly than we have judged ourselves. Yet this very acknowledgment, far from
weakening my opposition to the proposed annexation, furnishes the most
compelling evidence against it. If our republic has struggled—and at times
failed—to incorporate justly or to treat equitably tribal populations numbering
in the hundreds of thousands, under specific constitutional provisions designed
for that purpose, how can any reasonable man suppose we should succeed in
forcibly annexing two sovereign nations, each possessing established
governments, distinct political cultures, and populations numbering in the tens
of millions? 
The difficulties we have encountered in the smaller matter
demonstrate the impossibility of the larger. To incorporate Canada and Mexico,
whether by force or coercion, would violate that principle of consent which
animated our own separation from Britain and which forms the cornerstone of
legitimate government. Republican government, as I wrote in Federalist No. 10,
requires not merely appropriate scale but proper constitutional structure to
control the effects of faction. The proposed annexation would create not a
strengthened republic but an ungovernable empire, multiplying factions beyond
all capacity for republican management. How could that delicate balance of
powers—that system of checks and balances which I labored to construct at
Philadelphia—function across a territory of such vast extent, encompassing
peoples of such varied political traditions? 
The result could only be tyrannical centralization to
maintain control, or fragmentation into ungovernable discord. When I supported
the Louisiana Purchase and asserted our claim to West Florida, these involved
largely unsettled territories or disputed jurisdictions, not the subjugation of
free peoples under established governments. The path to national strength lies
not in abandoning principle because we have imperfectly applied it, but in
recognizing the limits of our capacity and perfecting our union within
sustainable bounds, rather than destroying it through imperial overreach that
would transform us into the very tyranny against which we fought to secure our
independence."""
    }
]

# --- END OF MANUAL INPUT SECTION ---


def display_final_report(judgment: dict, simple_arg: str, complex_arg: str):
    print("\n\n========================================================")
    print("                 A R B I T E R ' S   F I N A L   R E P O R T                  ")
    print("========================================================\n")
    
    data = judgment
    
    try:
        scores = data.get("scores", {})
        scores_a_data = scores.get("simple_model_argument_A", {})
        scores_b_data = scores.get("complex_model_argument_B", {})
        
        s_a_struct = scores_a_data.get("structure_score", "N/A")
        s_a_depth = scores_a_data.get("depth_score", "N/A")
        s_a_support = scores_a_data.get("support_score", "N/A")
        s_a_rhetoric = scores_a_data.get("rhetoric_score", "N/A")
        s_a_final = scores_a_data.get("final_score", "N/A")

        s_b_struct = scores_b_data.get("structure_score", "N/A")
        s_b_depth = scores_b_data.get("depth_score", "N/A")
        s_b_support = scores_b_data.get("support_score", "N/A")
        s_b_rhetoric = scores_b_data.get("rhetoric_score", "N/A")
        s_b_final = scores_b_data.get("final_score", "N/A")

        winner = data.get("winning_model", "N/A")
        justification = data.get("justification", "No justification provided.")
        
        print("--- SIMPLE MODEL OUTPUT ---\n")
        print(simple_arg)
        print("\n--- Arbiter's Score for Simple Model ---")
        print(f"  Final Score: {s_a_final} / 100")
        print(f"    - Structure: {s_a_struct}/10 | Depth: {s_a_depth}/10 | Support: {s_a_support}/10 | Rhetoric: {s_a_rhetoric}/10")

        print("\n\n--- COMPLEX MODEL OUTPUT ---\n")
        print(complex_arg)
        print("\n--- Arbiter's Score for Complex Model ---")
        print(f"  Final Score: {s_b_final} / 100")
        print(f"    - Structure: {s_b_struct}/10 | Depth: {s_b_depth}/10 | Support: {s_b_support}/10 | Rhetoric: {s_b_rhetoric}/10")

        print("\n\n---------------------------------")
        print("               V E R D I C T               ")
        print("---------------------------------")
        print(f"WINNER: {winner}")
        print("\nJustification:")
        print(justification)
        print("\n========================================================")

    except Exception as e:
        print("\n--- ERROR: COULD NOT PARSE THE ARBITER'S DETAILED REPORT ---")
        print(f"Error: {e}")
        print("Raw data received from the agent:")
        print(data)

def run_all_analyses():
    try:
        arbiter = ArbiterAgent()
        with open("prompts.yaml", "r", encoding='utf-8') as f:
            all_prompts = yaml.safe_load(f)
        arbiter_prompts = all_prompts['ArbiterAgent']
        system_prompt = arbiter_prompts['Hamilton']['system_prompt']
        user_prompt_template = arbiter_prompts['user_prompt_template']
    except Exception as e:
        print(f"ERROR during setup: {e}")
        return

    for i, debate in enumerate(debates_to_analyze):
        founder_name = debate["founder_name"]
        simple_argument = debate["simple_argument"].strip()
        complex_argument = debate["complex_argument"].strip()

        print(f"\n\n{'#'*25} ANALYSIS #{i+1}: {founder_name.upper()} {'#'*25}")

        if not simple_argument or "(Paste" in simple_argument:
            print(f"Skipping {founder_name}: One or both arguments are empty or placeholders.")
            continue

        user_prompt = user_prompt_template.format(simple_model_argument=simple_argument, complex_model_argument=complex_argument)

        print("\nCalling Arbiter Agent to evaluate the arguments...")
        judgment_output = arbiter.run(system_prompt, user_prompt)

        if "error" in judgment_output:
            print(f"\n--- ARBITER AGENT FAILED FOR {founder_name} ---")
            print(judgment_output.get("response", "No response text available."))
        else:
            display_final_report(judgment_output, simple_argument, complex_argument)
    
    print("\n\n--- All Analyses Complete ---")

if __name__ == "__main__":
    run_all_analyses()