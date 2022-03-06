import io

def write_model_summary(model):
    with io.StringIO() as stream:
        model.summary(print_fn=lambda x: stream.write(x + '\n'))
        summary_str= stream.getvalue()
    return summary_str