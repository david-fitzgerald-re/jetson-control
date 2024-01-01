<script>
	import { enhance } from '$app/forms';
	import toast, { Toaster } from 'svelte-french-toast';

	export let currentColour = 'unknown';
	export let etag = "";
	let selectedColour = 'red'; // Default selected color
	const colors = ['red', 'blue'];

	function handleSubmit() {
		// Handle submission logic here
		// You can send the selectedColor to the backend
		console.log('Selected Color:', selectedColour);
	}
</script>

<!-- TODO move this somewhere better? -->
<Toaster />

<div class="container">
	<form
		method="POST"
		use:enhance={({ formElement, formData, action, cancel, submitter }) => {
			// `formElement` is this `<form>` element
			// `formData` is its `FormData` object that's about to be submitted
			// `action` is the URL to which the form is posted
			// calling `cancel()` will prevent the submission
			// `submitter` is the `HTMLElement` that caused the form to be submitted
			
			const entries = [...formData.entries()];
			console.log(`Form data: ${entries}`);
			

			// const saveSettings = async (settings) => {
			//   await new Promise((resolve) => setTimeout(resolve, 1000));
			//   // If you want to return something, you can do it here
			// };
			// const settings = {}
			// toast.promise(
			//   saveSettings(settings),
			//   {
			//     loading: 'Saving...',
			//     success: 'Settings saved!',
			//     error: 'Could not save.',
			//   }
			// );

			
			return async ({ result, update }) => {
				console.log(result);
				switch (result.type) {
					case 'success':
						toast.success('Success');
						break;
					case 'failure':
						toast.error('Failed');
						cancel()
						break;
					default:
						break;
				}
				await update({ invalidateAll: false });
				// `result` is an `ActionResult` object
				// `update` is a function which triggers the default logic that would be triggered if this callback wasn't set
			};
		}}
	>
		<div class="table">
			<div class="cell">Colour</div>
			<div class="cell disabled">{currentColour}</div>
			<div class="cell">
				<select bind:value={selectedColour} name="colour" class="w-full">
					{#each colors as color}
						<option value={color}>{color}</option>
					{/each}
				</select>
			</div>
			<input bind:value={etag} type="hidden"/>
			<button on:click={handleSubmit} class="submit-btn mt-4">Submit</button>
		</div>
	</form>
</div>

<style>
	/* Additional custom styling can be added here */

	.container {
		max-width: 600px;
		margin: auto;
		padding: 2rem;
	}

	.table {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr 1fr;
		gap: 1rem;
	}

	.cell {
		padding: 1rem;
		border: 1px solid #ddd;
		border-radius: 0.25rem;
	}

	.disabled {
		background-color: #f2f2f2;
		color: #777;
	}

	.submit-btn {
		padding: 0.5rem 1rem;
		background-color: #4caf50;
		color: #fff;
		border: none;
		border-radius: 0.25rem;
		cursor: pointer;
	}

	form {
		display: grid;
	}
</style>
