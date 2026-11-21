using DanskeByer.Models;

namespace DanskeByer.Services;

public enum QuizPhase { Asking, Answered, Finished }

/// <summary>Pure game logic for "find the town (or sight) on the map" – no UI in here.</summary>
public sealed class QuizEngine(Random? random = null)
{
    public const int MaxAttempts = 3;

    private readonly Random _rng = random ?? Random.Shared;
    private List<QuizItem> _questions = [];
    private readonly HashSet<string> _wrong = [];

    public QuizPhase Phase { get; private set; } = QuizPhase.Finished;
    public int Index { get; private set; }
    public int Total => _questions.Count;
    public int Score { get; private set; }
    public int Attempts { get; private set; }
    public bool HintShown { get; private set; }
    public bool LastAnswerCorrect { get; private set; }
    public string? Feedback { get; private set; }
    /// <summary>All the questions in this round, in the order they are asked.</summary>
    public IReadOnlyList<QuizItem> Questions => _questions;
    public QuizItem? Current => Index < _questions.Count ? _questions[Index] : null;
    public IReadOnlySet<string> WrongIds => _wrong;
    public int AttemptsLeft => MaxAttempts - Attempts;

    /// <summary>Starts a quiz with the pool in random order; <paramref name="count"/> asks only that many of them.</summary>
    public void Start(IEnumerable<QuizItem> pool, int? count = null)
    {
        var shuffled = pool.OrderBy(_ => _rng.Next());
        _questions = (count is { } n ? shuffled.Take(n) : shuffled).ToList();
        Index = 0;
        Score = 0;
        ResetQuestion();
        Phase = _questions.Count > 0 ? QuizPhase.Asking : QuizPhase.Finished;
    }

    /// <summary>Handles a click on a town dot. Returns true if it was the right one.</summary>
    public bool Guess(Town clicked) => Guess(clicked.Id, clicked.Name, clicked);

    /// <summary>Handles a click on a sight star. Returns true if it was the right one.</summary>
    public bool Guess(Sight clicked) => Guess(clicked.Id, clicked.Name, clicked);

    private bool Guess(string id, string name, IPlace clicked)
    {
        if (Phase != QuizPhase.Asking || Current is not { } answer) return false;

        if (id == answer.Id)
        {
            Score++;
            LastAnswerCorrect = true;
            Feedback = Attempts == 0 ? "Rigtigt! 🎉" : "Rigtigt til sidst! 👍";
            Phase = QuizPhase.Answered;
            return true;
        }

        if (!_wrong.Add(id)) return false;   // same wrong dot twice does not cost a try
        Attempts++;
        if (Attempts >= MaxAttempts)
        {
            LastAnswerCorrect = false;
            Feedback = "Det var desværre ikke rigtigt. Her er svaret:";
            Phase = QuizPhase.Answered;
        }
        else
        {
            var dir = Geo.Direction(clicked, answer);
            var d = Geo.DistanceKm(clicked, answer);
            var km = d < 10 ? Math.Max(1, (int)Math.Round(d)) : (int)Math.Round(d / 5) * 5;
            Feedback = $"Det var {name}. {answer.Kind} du søger ligger mod {dir} herfra – ca. {km} km væk.";
        }
        return false;
    }

    public void ShowHint()
    {
        if (Phase == QuizPhase.Asking) HintShown = true;
    }

    /// <summary>Give up on this question (no point) and show the answer.</summary>
    public void Skip()
    {
        if (Phase != QuizPhase.Asking) return;
        LastAnswerCorrect = false;
        Feedback = "Ingen point denne gang. Her er svaret:";
        Phase = QuizPhase.Answered;
    }

    public void Next()
    {
        if (Phase != QuizPhase.Answered) return;
        Index++;
        ResetQuestion();
        Phase = Index >= _questions.Count ? QuizPhase.Finished : QuizPhase.Asking;
    }

    private void ResetQuestion()
    {
        Attempts = 0;
        HintShown = false;
        LastAnswerCorrect = false;
        Feedback = null;
        _wrong.Clear();
    }

    public string Verdict()
    {
        if (Total == 0) return "";
        var ratio = (double)Score / Total;
        return ratio switch
        {
            >= 1.0 => "Perfekt! Du kender hele Danmark! 🏆",
            >= 0.8 => "Super flot! Du er en rigtig Danmarks-ekspert! 🌟",
            >= 0.5 => "Godt klaret! Prøv igen og slå din rekord. 👍",
            _ => "God træning! Prøv igen – du bliver bedre og bedre. 💪",
        };
    }
}
