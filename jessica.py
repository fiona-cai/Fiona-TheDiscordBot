from autocorrect import Speller
import pkg_resources
from symspellpy import SymSpell
from discord.ext import commands
from PyDictionary import PyDictionary

spell = Speller()
dictionary = PyDictionary()


class Jessica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jessica",
                      aliases=["autocorrect", "correct", "auto", "hessica"])
    async def jessica(self, ctx):
        input_term = await ctx.channel.fetch_message(
            ctx.message.reference.message_id)
        sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        dictionary_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_dictionary_en_82_765.txt")
        bigram_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
        sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
        sym_spell.load_bigram_dictionary(bigram_path,
                                         term_index=0,
                                         count_index=2)

        suggestions = sym_spell.lookup_compound(input_term.content,
                                                max_edit_distance=2)
        for suggestion in suggestions:
            print(suggestion.term)
            await ctx.reply(suggestion.term)

    @commands.command(name="sauto")
    async def sauto(self, ctx):
        print("hi")
        input_term = await ctx.channel.fetch_message(
            ctx.message.reference.message_id)
        await ctx.reply(spell(input_term.content))


def setup(bot):
    bot.add_cog(Jessica(bot))
